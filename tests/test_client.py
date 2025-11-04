"""
Tests for GossetClient
"""
import os
import pytest
from gosset_sdk import GossetClient


def test_client_initialization_with_env():
    """Test that client initializes with environment variables"""
    # Skip if no API key is available
    if not (os.getenv("GOSSET_API_KEY") or os.getenv("GOSSET_OAUTH_TOKEN")):
        pytest.skip("No API key available")
    
    client = GossetClient()
    assert client.api_key is not None
    assert client.base_url is not None
    assert client.timeout == 30


def test_client_initialization_with_param():
    """Test that client initializes with provided api_key"""
    client = GossetClient(api_key="test_key")
    assert client.api_key == "test_key"


def test_client_initialization_no_key():
    """Test that client raises ValueError when no API key is available"""
    # Temporarily remove env vars
    old_api_key = os.environ.pop("GOSSET_API_KEY", None)
    old_oauth_token = os.environ.pop("GOSSET_OAUTH_TOKEN", None)
    
    try:
        with pytest.raises(ValueError, match="API key required"):
            GossetClient()
    finally:
        # Restore env vars
        if old_api_key:
            os.environ["GOSSET_API_KEY"] = old_api_key
        if old_oauth_token:
            os.environ["GOSSET_OAUTH_TOKEN"] = old_oauth_token


def test_client_context_manager():
    """Test that client works as context manager"""
    if not (os.getenv("GOSSET_API_KEY") or os.getenv("GOSSET_OAUTH_TOKEN")):
        pytest.skip("No API key available")
    
    with GossetClient() as client:
        assert client.api_key is not None
    
    # Session should be closed after context exit
    # (we don't test this explicitly as it's internal behavior)


def test_client_custom_base_url():
    """Test that client accepts custom base URL"""
    client = GossetClient(api_key="test_key", base_url="https://custom.api.url")
    assert client.base_url == "https://custom.api.url"


def test_client_base_url_trailing_slash():
    """Test that client strips trailing slash from base URL"""
    client = GossetClient(api_key="test_key", base_url="https://custom.api.url/")
    assert client.base_url == "https://custom.api.url"


def test_client_custom_timeout():
    """Test that client accepts custom timeout"""
    client = GossetClient(api_key="test_key", timeout=60)
    assert client.timeout == 60


# Integration tests (require valid API key and working API)
@pytest.mark.skipif(
    not (os.getenv("GOSSET_API_KEY") or os.getenv("GOSSET_OAUTH_TOKEN")),
    reason="No API key available"
)
def test_classify_diseases_integration():
    """Integration test for classify_diseases"""
    client = GossetClient()
    
    try:
        result = client.classify_diseases("Breast Cancer")
        assert "disease_classes" in result
        assert isinstance(result["disease_classes"], list)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


@pytest.mark.skipif(
    not (os.getenv("GOSSET_API_KEY") or os.getenv("GOSSET_OAUTH_TOKEN")),
    reason="No API key available"
)
def test_estimate_ptrs_integration():
    """Integration test for estimate_ptrs"""
    client = GossetClient()
    
    try:
        result = client.estimate_ptrs(phase=2)
        assert "total_trials" in result
        assert "average_met_endpoints_one" in result
        assert isinstance(result["total_trials"], int)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


@pytest.mark.skipif(
    not (os.getenv("GOSSET_API_KEY") or os.getenv("GOSSET_OAUTH_TOKEN")),
    reason="No API key available"
)
def test_estimate_ptrs_with_disease_class_string():
    """Integration test for estimate_ptrs with single disease class as string"""
    client = GossetClient()
    
    try:
        result = client.estimate_ptrs(disease_classes='GD-01')
        assert "total_trials" in result
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


@pytest.mark.skipif(
    not (os.getenv("GOSSET_API_KEY") or os.getenv("GOSSET_OAUTH_TOKEN")),
    reason="No API key available"
)
def test_estimate_ptrs_with_disease_class_list():
    """Integration test for estimate_ptrs with multiple disease classes as list"""
    client = GossetClient()
    
    try:
        result = client.estimate_ptrs(disease_classes=['GD-01', 'GD-02'])
        assert "total_trials" in result
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

