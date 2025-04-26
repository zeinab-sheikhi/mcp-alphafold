import csv
import hashlib
import json
import os
from io import StringIO
from ssl import PROTOCOL_TLS_CLIENT, SSLContext, TLSVersion
from typing import (
    Any,
    Dict,
    Literal,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import httpx
from diskcache import Cache
from platformdirs import user_cache_dir
from pydantic import BaseModel

from mcp_alphafold.config import settings

_cache: Optional[Cache] = None
T = TypeVar("T", bound=BaseModel)


class RequestError(BaseModel):
    code: int
    message: str


def get_ssl_context(
    cert_file: Optional[str] = None,
    key_file: Optional[str] = None,
    tls_version: TLSVersion = TLSVersion.TLSv1_3,
) -> SSLContext:
    """Create an SSLContext with the specified TLS version."""

    cert_file_path = cert_file or settings.SSL_CERT_FILE
    key_file_path = key_file or settings.SSL_KEY_FILE

    if not cert_file_path:
        raise ValueError("Certificate file path not provided and SSL_CERT_FILE environment variable not set")
    if not key_file_path:
        raise ValueError("Key file path not provided and SSL_KEY_FILE environment variable not set")

    if not os.path.exists(cert_file_path):
        raise FileNotFoundError(f"Certificate file not found at {cert_file_path}")
    if not os.path.exists(key_file_path):
        raise FileNotFoundError(f"Key file not found at {key_file_path}")

    context = SSLContext(PROTOCOL_TLS_CLIENT)
    context.load_cert_chain(certfile=cert_file_path, keyfile=key_file_path)
    context.maximum_version = tls_version
    context.minimum_version = tls_version
    context.load_verify_locations(cafile=cert_file_path)
    context.check_hostname = False  # disable for testing purposes
    return context


def get_cache() -> Cache:
    """Initialize and return the cache."""
    global _cache
    if _cache is None:
        cache_path = os.path.join(
            settings.CACHE_DIR or user_cache_dir("alphafold-mcp"),
            "cache",
        )
        _cache = Cache(cache_path)
    return _cache


def generate_cache_key(
    method: str,
    url: str,
    params: Optional[Dict[str, Any]] = None,
) -> str:
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
    params: Optional[Dict[str, Any]] = None,
    verify: Union[SSLContext, str, bool] = False,
    timeout: Optional[int] = None,
) -> Tuple[int, str]:
    """Perform an HTTP request(GET/POST)."""
    timeout = timeout or settings.REQUEST_TIMEOUT
    try:
        async with httpx.AsyncClient(
            verify=verify,
            http2=False,
            timeout=timeout,
        ) as client:
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
    cache_ttl: Optional[int] = None,
    tls_version: Optional[TLSVersion] = TLSVersion.TLSv1_3,
) -> Tuple[Optional[T], Optional[RequestError]]:
    """Request API with caching logic"""

    cache_ttl = cache_ttl or settings.CACHE_TTL
    verify: Union[SSLContext, str, bool] = False
    if tls_version:
        ssl_context = get_ssl_context(tls_version=tls_version)
        verify = ssl_context

    params: Optional[Dict[str, Any]] = None

    # convert request to param dict
    if request is not None:
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


def parse_response(
    status_code: int,
    content: str,
    response_model_type: Optional[Type[T]] = None,
) -> Tuple[Optional[T], Optional[RequestError]]:
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
