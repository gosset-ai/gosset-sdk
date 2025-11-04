#!/usr/bin/env python3
"""
Quick test to verify GossetClient can be imported and initialized
"""

def test_import():
    """Test that the client can be imported"""
    try:
        from gosset_sdk import GossetClient, GossetAPIError
        print("✓ Successfully imported GossetClient and GossetAPIError")
        return True
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return False

def test_initialization():
    """Test that the client can be initialized"""
    try:
        from gosset_sdk import GossetClient
        
        # Test with explicit API key
        client = GossetClient(api_key="test_key_123")
        print("✓ Successfully initialized GossetClient with API key")
        
        # Verify attributes
        assert client.api_key == "test_key_123"
        assert client.base_url == "https://api-dev.gosset.ai"
        assert client.timeout == 30
        print("✓ Client attributes are correct")
        
        # Test context manager
        with GossetClient(api_key="test_key_456") as client2:
            assert client2.api_key == "test_key_456"
        print("✓ Context manager works")
        
        return True
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handling():
    """Test that proper errors are raised"""
    try:
        from gosset_sdk import GossetClient
        
        # Test missing API key
        try:
            import os
            # Save current env var if it exists
            saved_key = os.environ.pop("GOSSET_API_KEY", None)
            
            client = GossetClient()
            print("✗ Should have raised ValueError for missing API key")
            
            # Restore env var
            if saved_key:
                os.environ["GOSSET_API_KEY"] = saved_key
            
            return False
        except ValueError as e:
            if "API key is required" in str(e):
                print("✓ Correctly raises ValueError for missing API key")
            else:
                print(f"✗ Wrong error message: {e}")
                return False
            
            # Restore env var
            if saved_key:
                os.environ["GOSSET_API_KEY"] = saved_key
        
        return True
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("GossetClient Import and Initialization Test")
    print("=" * 60)
    print()
    
    tests = [
        ("Import test", test_import),
        ("Initialization test", test_initialization),
        ("Error handling test", test_error_handling),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"Running: {name}")
        print("-" * 60)
        result = test_func()
        results.append((name, result))
        print()
    
    print("=" * 60)
    print("Test Results:")
    print("=" * 60)
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
    
    all_passed = all(result for _, result in results)
    print()
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())

