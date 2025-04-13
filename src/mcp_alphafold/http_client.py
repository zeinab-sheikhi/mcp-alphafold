import csv
import hashlib
import json
import os 
from io import StringIO
from ssl import SSLContext, PROTOCOL_TLS_CLIENT, TLSVersion
from typing import Any, Dict, Literal, Optional, Type, TypeVar, Tuple, Union

import httpx
from diskcache import Cache
from dotenv import load_dotenv
from platformdirs import user_cache_dir
from pydantic import BaseModel


load_dotenv()

_cache: Optional[Cache] = None
T = TypeVar("T", bound=BaseModel)


class RequestError(BaseModel):
    code: int
    message: str


def get_ssl_context(cert_file: str = None, key_file: str = None, tls_version: TLSVersion = TLSVersion.TLSv1_3) -> SSLContext:
    """Create an SSLContext with the specified TLS version."""
    
    cert_file = cert_file or os.getenv("SSL_CERT_FILE")
    key_file = key_file or os.getenv("SSL_KEY_FILE")
    
    if not os.path.exists(cert_file):
        raise FileNotFoundError(f"Certificate file not found at {cert_file}")
    if not os.path.exists(key_file):
        raise FileNotFoundError(f"Key file not found at {key_file}")

    context = SSLContext(PROTOCOL_TLS_CLIENT)
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    context.maximum_version = tls_version
    context.minimum_version = tls_version
    context.load_verify_locations(cafile=cert_file)
    context.check_hostname = False  # disable for testing purposes
    return context


def get_cache() -> Cache:
    """Initialize and return the cache."""
    global _cache
    if _cache is None:
        cache_path = os.path.join(user_cache_dir("alphafold-mcp"), "cache")
        _cache = Cache(cache_path)
    return _cache


def generate_cache_key(method: str, url: str, params: dict) -> str:
    """Generate a cache key for a given HTTP request."""
    sha256_hash = hashlib.sha256()
    params_dump: str = json.dumps(params, sort_keys=True)
    key_source: str = f"{method.upper()}:{url}:{params_dump}"
    data: bytes = key_source.encode("utf-8")
    sha256_hash.update(data)
    return sha256_hash.hexdigest()


def get_cache_response(cache_key: str) -> Optional[str]:
    """Retrieve the cache response if avialable."""
    cache = get_cache()
    return cache.get(cache_key)


def cache_response(cache_key: str, content: str, cache_ttl: int) -> None:
    """Store the response content in cache."""
    cache = get_cache()
    cache.set(cache_key, content, expire=cache_ttl)


async def call_http(
        method: str, 
        url: str, 
        params: Optional[dict] = None, 
        verify: Union[SSLContext, str, bool] = False
) -> tuple[int, str]:
    """Perform an HTTP request(GET/POST)."""
    try:
        async with httpx.AsyncClient(verify=verify, http2=False) as client:
            if method.upper() == "GET":
                resp = await client.get(url, params=params)
            elif method.upper() == "POST":
                resp = await client.post(url, json=params or {})
            else:
                return 405, f"Unsupported Mehtod: {method}"
            return resp.status_code, resp.text

    except httpx.HTTPError as e:
        return 599, str(e)
    

async def request_api(
        url: str, 
        request: Optional[Union[BaseModel, Dict]] = None,
        response_model_type: Optional[Type[T]] = None, 
        method: Literal["GET", "POST"] = "GET",
        cache_ttl: int = 86400, 
        tls_version: Optional[TLSVersion] = TLSVersion.TLSv1_3,
) -> Tuple[Optional[T], Optional[RequestError]]:
    """Request API with caching logic"""
    
    verify = get_ssl_context(tls_version=tls_version) if tls_version else False

    params: Optional[Dict[str, Any]] = None
    # convert request to param dict
    if method == "POST" and request is not None:
        if isinstance(request, BaseModel):
            params = request.model_dump(exclude_none=True, by_alias=True)
        else:
            params = request

    # Short-Circuit if caching is not enabled
    if cache_ttl == 0:
        status, content = await call_http(
            method=method,
            url=url,
            params=params,
            verify=verify,
        )
        return parse_response(status, content, response_model_type)
    
    # caching enable 
    cache_key = generate_cache_key(method=method, url=url, params=params)
    cached_content = get_cache_response(cache_key=cache_key)

    if cached_content: 
        return parse_response(200, cached_content, response_model_type)
    
    # Make HTTP request if not cached
    status, content = await call_http(
        method=method, 
        url=url, 
        params=params, 
        verify=verify,
    )
    parsed_response = parse_response(status, content, response_model_type)

    if status == 200:
        cache_response(cache_key, content, cache_ttl)
    
    return parsed_response


def parse_response(status_code: int, content: str, response_model_type: Optional[Type[T]] = None) -> Tuple[Optional[T], Optional[RequestError]]:
    """Parse the HTTP response based on the status code"""
    if status_code != 200:
        return None, RequestError(code=status_code, message=content)
    try:
        if response_model_type is None:
            if content.startswith("{") or content.startswith("["):
                response_dict = json.loads(content)
            elif "," in content:
                io = StringIO(content)
                response_dict = list(csv.DictReader(io))
            else:
                response_dict = {"text": content}
            return response_dict, None
        parsed: T = response_model_type.model_validate_json(content)
        return parsed, None
    except Exception as e:
        return None, RequestError(code=500, message=str(e))
