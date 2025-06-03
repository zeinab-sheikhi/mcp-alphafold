import json
import os

import httpx
import pytest
from diskcache import Cache
from pydantic import BaseModel

from mcp_alphafold.utils.http import (
    RequestError,
    cache_response,
    call_http,
    generate_cache_key,
    get_cache,
    get_cache_response,
    parse_response,
)


@pytest.mark.skip(reason="Model class, not a test class")
class ResponseModel(BaseModel):
    name: str
    value: int


@pytest.mark.parametrize(
    "status_code, content, model, expected_result, expected_error",
    [
        # Test successful JSON response with model
        (
            200,
            '{"name": "test", "value": 42}',
            ResponseModel,
            ResponseModel(name="test", value=42),
            None,
        ),
        # Test successful JSON response without model
        (
            200,
            '{"key": "value"}',
            None,
            {"key": "value"},
            None,
        ),
        # Test successful CSV response
        (
            200,
            "name,value\ntest,42",
            None,
            [{"name": "test", "value": "42"}],
            None,
        ),
        # Test plain text response
        (
            200,
            "Hello World",
            None,
            {"text": "Hello World"},
            None,
        ),
        # Test error status code
        (
            404,
            "Not Found",
            None,
            None,
            RequestError(code=404, message="Not Found"),
        ),
    ],
)
def test_parse_response(status_code, content, model, expected_result, expected_error):
    """Test parse_response with different inputs and expected outputs."""
    result, error = parse_response(status_code, content, model)

    if expected_error:
        assert error is not None
        assert error.code == expected_error.code
        assert error.message == expected_error.message
        assert result is None
    else:
        assert error is None
        assert result == expected_result


@pytest.mark.parametrize(
    "method, url, params, expected_prefix",
    [
        # Test basic GET request
        (
            "GET",
            "https://api.example.com",
            {"key": "value"},
            "GET:https://api.example.com:{",
        ),
        # Test POST request
        (
            "post",  # Test case-insensitive handling
            "https://api.example.com/data",
            {"id": 123},
            "POST:https://api.example.com/data:{",
        ),
        # Test with empty params
        (
            "GET",
            "https://api.example.com",
            {},
            "GET:https://api.example.com:{}",
        ),
        # Test with nested params
        (
            "GET",
            "https://api.example.com",
            {"filter": {"name": "test", "value": 42}},
            "GET:https://api.example.com:{",
        ),
    ],
)
def test_generate_cache_key(method, url, params, expected_prefix):
    """Test cache key generation with different inputs."""
    cache_key = generate_cache_key(method, url, params)

    # Verify it's a valid SHA-256 hash (64 characters, hexadecimal)
    assert len(cache_key) == 64
    assert all(c in "0123456789abcdef" for c in cache_key)

    # Verify the key is deterministic (same input produces same output)
    assert cache_key == generate_cache_key(method, url, params)

    # Verify the key source format
    key_source = f"{method.upper()}:{url}:{params}"
    assert key_source.startswith(expected_prefix)


@pytest.fixture
def mock_cache_dir(tmp_path, monkeypatch):
    """Create a temporary cache directory and patch user_cache_dir."""
    cache_dir = tmp_path / "cache"
    # Create the directory if it doesn't exist
    cache_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("mcp_alphafold.utils.http.user_cache_dir", lambda x: str(tmp_path))
    return cache_dir


def test_get_cache_initialization(mock_cache_dir):
    """Test cache initialization."""
    # First call should create cache
    cache = get_cache()
    assert isinstance(cache, Cache)
    assert os.path.exists(mock_cache_dir)

    # Second call should return same cache instance
    cache2 = get_cache()
    assert cache is cache2


def test_cache_operations(mock_cache_dir):
    """Test storing and retrieving values from cache."""
    # Test data
    key = "test_key"
    content = "test_content"
    ttl = 3600  # 1 hour

    # Store in cache
    cache_response(key, content, ttl)

    # Retrieve from cache
    cached_content = get_cache_response(key)
    assert cached_content == content

    # Test non-existent key
    assert get_cache_response("nonexistent_key") is None


def test_cache_expiration(mock_cache_dir):
    """Test cache expiration."""
    key = "expiring_key"
    content = "expiring_content"
    ttl = 0  # Expire immediately

    # Store with zero TTL
    cache_response(key, content, ttl)

    # Should be expired
    assert get_cache_response(key) is None


def test_cache_different_types(mock_cache_dir):
    """Test caching different types of content."""
    test_cases = [
        ("string_key", "simple string"),
        ("json_key", '{"key": "value"}'),
        ("number_key", "42"),
        ("unicode_key", "Hello 世界"),
    ]

    for key, content in test_cases:
        cache_response(key, content, 3600)
        assert get_cache_response(key) == content


@pytest.mark.asyncio
async def test_call_http_get_success(httpx_mock):
    """Test successful GET request."""
    # Mock successful response
    httpx_mock.add_response(status_code=200, text="success response")

    status, content = await call_http(method="GET", url="https://api.example.com", params={"key": "value"})

    assert status == 200
    assert content == "success response"

    # Verify request was made correctly
    request = httpx_mock.get_request()
    assert request.method == "GET"
    assert request.url.params["key"] == "value"


@pytest.mark.asyncio
async def test_call_http_post_success(httpx_mock):
    """Test successful POST request."""
    # Mock successful response
    httpx_mock.add_response(status_code=201, text="created")

    status, content = await call_http(method="POST", url="https://api.example.com", params={"data": "test"})

    assert status == 201
    assert content == "created"

    # Verify request was made correctly
    request = httpx_mock.get_request()
    assert request.method == "POST"
    assert json.loads(request.content) == {"data": "test"}


@pytest.mark.asyncio
async def test_call_http_error_response(httpx_mock):
    """Test handling of error responses."""
    # Mock error response
    httpx_mock.add_response(status_code=404, text="not found")

    status, content = await call_http(method="GET", url="https://api.example.com")

    assert status == 404
    assert content == "not found"


@pytest.mark.asyncio
async def test_call_http_network_error(httpx_mock):
    """Test handling of network errors."""
    # Mock network error
    for _ in range(4):  # Match the number of retry attempts
        httpx_mock.add_exception(httpx.ConnectError("Connection failed"))

    status, content = await call_http(method="GET", url="https://api.example.com")

    assert status == 599


@pytest.mark.asyncio
async def test_call_http_unsupported_method(httpx_mock):
    """Test handling of unsupported HTTP methods."""
    status, content = await call_http(
        method="PUT",  # Unsupported method
        url="https://api.example.com",
    )

    assert status == 405
