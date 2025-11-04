"""
Minimal example of using GossetClient for PTRs and disease classification.

Quick reference showing the essential code needed.
"""

from gosset import GossetClient

# Initialize client (uses GOSSET_API_KEY or GOSSET_OAUTH_TOKEN from environment)
client = GossetClient()

# Example 1: Classify a disease
print("\n=== Classify Disease: Breast Cancer ===")
result = client.classify_diseases("Breast Cancer")
disease_classes = result['disease_classes']
print(f"Disease classes: {disease_classes}")

# Example 2: Query Phase 2 trials
print("\n=== Phase 2 Trials ===")
stats = client.estimate_ptrs(phase=2)
print(f"Total trials: {stats['total_trials']}")
print(f"Trials with endpoint data: {stats['trials_with_endpoint_data']}")
print(f"Average met endpoints (one): {stats['average_met_endpoints_one']:.2%}")
print(f"Average progressed: {stats['average_progressed']:.2%}")
print(f"Average arm size: {stats['average_arm_size']:.1f}")

# Example 3: Query with disease class (string or list)
print("\n=== Disease Class: GD-01 ===")
stats = client.estimate_ptrs(disease_classes='GD-01')
print(f"Total trials: {stats['total_trials']}")
print(f"Average met endpoints (one): {stats['average_met_endpoints_one']:.2%}")

# Example 4: Combine filters (Phase 2 + Disease Class)
print("\n=== Phase 2 + Disease Class: GD-01 ===")
stats = client.estimate_ptrs(disease_classes='GD-01', phase=2)
print(f"Total trials (Phase 2 in GD-01): {stats['total_trials']}")
print(f"Trials with endpoint data: {stats['trials_with_endpoint_data']}")
print(f"Average met endpoints (one): {stats['average_met_endpoints_one']:.2%}")
print(f"Average met endpoints (all): {stats['average_met_endpoints_all']:.2%}")
print(f"Average progressed: {stats['average_progressed']:.2%}")

# Example 5: Multiple disease classes
print("\n=== Multiple Disease Classes: GD-01 and GD-02 ===")
stats = client.estimate_ptrs(disease_classes=['GD-01', 'GD-02'])
print(f"Total trials: {stats['total_trials']}")
print(f"Average met endpoints (one): {stats['average_met_endpoints_one']:.2%}")

print("\n✓ Done!")

# Clean up
client.close()

