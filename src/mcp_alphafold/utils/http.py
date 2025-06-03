import asyncio
import csv
import hashlib
import json
import logging
import os
import random
from io import StringIO
from typing import Any, Dict, Literal, Optional, Tuple, Type, TypeVar, Union

import httpx
from diskcache import Cache
from platformdirs import user_cache_dir
from pydantic import BaseModel

from mcp_alphafold.settings import settings

logger = logging.getLogger(__name__)
_cache: Optional[Cache] = None
T = TypeVar("T", bound=BaseModel)


class RequestError(BaseModel):
    code: int
    message: str


# --------------------------------
# CACHING
# --------------------------------
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
    return get_cache().get(cache_key)


def cache_response(cache_key: str, content: str, cache_ttl: int) -> None:
    """Store the response content in cache."""
    get_cache().set(cache_key, content, expire=cache_ttl)


# --------------------------------
# HTTP REQUEST
# --------------------------------
async def call_http(
    method: str,
    url: str,
    params: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = None,
    retries: int = 3,
    backoff_factor: float = 0.5,
    rate_limit_delay: Optional[float] = None,
) -> Tuple[int, str]:
    """Perform an HTTP request(GET/POST) with retries and optional rate limit."""
    timeout = timeout or settings.REQUEST_TIMEOUT

    if rate_limit_delay:
        await asyncio.sleep(rate_limit_delay)

    last_error: Optional[Exception] = None
    for attempt in range(retries + 1):
        try:
            async with httpx.AsyncClient(
                verify=False,
                http2=False,
                timeout=timeout,
                trust_env=False,
            ) as client:
                if method.upper() == "GET":
                    resp = await client.get(url, params=params)
                elif method.upper() == "POST":
                    resp = await client.post(url, json=params or {})
                else:
                    logger.error(f"Unsupported HTTP method: {method}")
                    return 405, f"Unsupported Method: {method}"

                return resp.status_code, resp.text

        except (httpx.RequestError, httpx.TimeoutException) as e:
            last_error = e
            if attempt < retries:  # Not the last attempt
                backoff = backoff_factor * (2**attempt) + random.uniform(0, 0.1)
                logger.warning(f"Request failed (attempt {attempt + 1}/{retries + 1}): {str(e)}")
                await asyncio.sleep(backoff)
            else:
                logger.error(f"Request failed after {retries + 1} attempts: {str(e)}")

    return 599, f"All retry attempts failed: {str(last_error)}"


# --------------------------------
# HIGH LEVEL REQUEST API
# --------------------------------
async def request_api(
    url: str,
    request: Optional[Union[BaseModel, Dict]] = None,
    response_model_type: Optional[Type[T]] = None,
    method: Literal["GET", "POST"] = "GET",
    cache_ttl: Optional[int] = None,
    retries: int = 3,
    rate_limit_delay: Optional[float] = None,
) -> Tuple[Optional[T], Optional[RequestError]]:
    """Main method for API request with cache, retry, and parsing."""

    cache_ttl = cache_ttl or settings.CACHE_TTL
    params: Optional[Dict[str, Any]] = None

    # Build request params
    if request is not None:
        if isinstance(request, BaseModel):
            params = request.model_dump(exclude_none=True, by_alias=True)
        else:
            params = request

    # No cache: always make the request
    if cache_ttl == 0:
        status, content = await call_http(
            method=method,
            url=url,
            params=params,
            retries=retries,
            rate_limit_delay=rate_limit_delay,
        )
        return parse_response(status, content, response_model_type)

    # Handle caching
    cache_key = generate_cache_key(method=method, url=url, params=params)
    cached_content = get_cache_response(cache_key=cache_key)
    if cached_content:
        return parse_response(200, cached_content, response_model_type)

    # Not cached, make HTTP request
    status, content = await call_http(
        method=method,
        url=url,
        params=params,
        retries=retries,
        rate_limit_delay=rate_limit_delay,
    )
    parsed_response = parse_response(status, content, response_model_type)

    if status == 200:
        cache_response(cache_key, content, cache_ttl)

    return parsed_response


# --------------------------------
# RESPONSE PARSING
# --------------------------------
def parse_response(
    status_code: int,
    content: str,
    response_model_type: Optional[Type[T]] = None,
) -> Tuple[Optional[T], Optional[RequestError]]:
    """Parse the HTTP response based on the content type."""
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
        return response_model_type.model_validate_json(content), None

    except Exception as e:
        logger.exception("Error parsing HTTP response")
        return None, RequestError(code=500, message=str(e))
