#!/usr/bin/env python3
"""
Quick test script to verify gosset-sdk installation
"""
import sys

def test_import():
    """Test package import"""
    try:
        from gosset import get_oauth_token, __version__
        print(f"✓ Package import successful (v{__version__})")
        return True
    except ImportError as e:
        print(f"✗ Package import failed: {e}")
        return False

def test_cli():
    """Test CLI availability"""
    import subprocess
    try:
        result = subprocess.run(
            ["gosset", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ CLI command available: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ CLI command failed with code {result.returncode}")
            return False
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        return False

def test_auth_module():
    """Test auth module is accessible"""
    try:
        from gosset.auth import get_oauth_token
        print("✓ Auth module accessible")
        return True
    except ImportError as e:
        print(f"✗ Auth module import failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Testing Gosset SDK Installation")
    print("=" * 60)
    print()
    
    tests = [
        ("Package Import", test_import),
        ("CLI Command", test_cli),
        ("Auth Module", test_auth_module),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"Testing {name}...")
        result = test_func()
        results.append(result)
        print()
    
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ All tests passed ({passed}/{total})")
        print("=" * 60)
        print("\nGosset SDK is ready to use!")
        print("\nNext steps:")
        print("  1. Get your token: gosset get-token")
        print("  2. Set environment: export GOSSET_OAUTH_TOKEN='your_token'")
        print("  3. Run example: python examples/biotech_agent.py")
        return 0
    else:
        print(f"✗ Some tests failed ({passed}/{total} passed)")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())

