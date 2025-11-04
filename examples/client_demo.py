"""
Example demonstrating the GossetClient for disease classification and PTRs.

This script shows how to:
1. Initialize the GossetClient
2. Classify diseases to get disease class IDs
3. Query PTRs (aggregate trial statistics) with different filters

PREREQUISITES:
- Set GOSSET_API_KEY or GOSSET_OAUTH_TOKEN in your environment
- Optional: Set GOSSET_API_URL (defaults to https://api.gosset.ai)

USAGE:
    python examples/client_demo.py
"""

from gosset import GossetClient


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}\n")


def print_stats(stats):
    """Pretty print aggregate trial statistics."""
    print(f"Trial Counts:")
    print(f"  Total Trials: {stats['total_trials']}")
    print(f"  Trials with Endpoint Data: {stats['trials_with_endpoint_data']}")
    print(f"  Trials with Comparator: {stats['trials_with_comparator']}")
    print(f"  Multi-arm Trials: {stats['multi_arm_trials']}")
    print(f"  Trials with Genomics: {stats['trials_with_genomics']}")
    print(f"  Trials with Biomarkers: {stats['trials_with_biomarkers']}")
    
    print(f"\nSuccess Rates (Averages):")
    print(f"  Met Endpoints (One): {stats['average_met_endpoints_one']:.1%}")
    print(f"  Met Endpoints (All): {stats['average_met_endpoints_all']:.1%}")
    print(f"  Progressed: {stats['average_progressed']:.1%}")
    
    print(f"\nOther Metrics:")
    print(f"  Average Arm Size: {stats['average_arm_size']:.1f}")


def main():
    """Main demonstration function."""
    
    # Initialize client (will use environment variables for API key)
    try:
        client = GossetClient()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease set GOSSET_API_KEY or GOSSET_OAUTH_TOKEN environment variable:")
        print("  export GOSSET_API_KEY='your_api_key_here'")
        return
    
    print("GossetClient Demonstration")
    print_section("Client initialized successfully")
    print(f"API URL: {client.base_url}")
    print(f"API Key: {'*' * (len(client.api_key) - 4)}{client.api_key[-4:] if len(client.api_key) > 4 else '****'}")
    
    # Example 1: Classify a disease
    print_section("1. Classify Disease: Breast Cancer")
    try:
        classification = client.classify_diseases("Breast Cancer")
        print(f"Disease classes: {classification.get('disease_classes', [])}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Basic PTRs query without filters
    print_section("2. PTRs Query: All Trials (No filters)")
    try:
        stats = client.estimate_ptrs()
        print_stats(stats)
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Filter by Phase 2
    print_section("3. PTRs Query: Phase 2 Trials")
    try:
        stats = client.estimate_ptrs(phase=2)
        print_stats(stats)
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Filter by disease class (single string)
    print_section("4. PTRs Query: Disease Class GD-01")
    try:
        stats = client.estimate_ptrs(disease_classes='GD-01')
        print_stats(stats)
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 5: Combine filters
    print_section("5. PTRs Query: Phase 2 + Disease Class GD-01")
    try:
        stats = client.estimate_ptrs(disease_classes='GD-01', phase=2)
        print_stats(stats)
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 6: Multiple disease classes
    print_section("6. PTRs Query: Multiple Disease Classes (GD-01 + GD-02)")
    try:
        stats = client.estimate_ptrs(disease_classes=['GD-01', 'GD-02'])
        print_stats(stats)
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 7: Using context manager
    print_section("7. Using Context Manager")
    try:
        with GossetClient() as client_ctx:
            result = client_ctx.classify_diseases("Alzheimer's Disease")
            print(f"Disease classes: {result['disease_classes']}")
    except Exception as e:
        print(f"Error: {e}")
    
    print_section("✓ Demonstration Complete!")
    
    # Clean up
    client.close()


if __name__ == '__main__':
    main()

