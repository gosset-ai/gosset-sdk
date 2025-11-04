# GossetClient Guide

Quick reference for using the GossetClient to interact with Gosset API endpoints.

## Overview

The `GossetClient` provides programmatic access to Gosset API endpoints for:
- **Disease Classification**: Map disease names to Gosset Disease (GD) classification IDs
- **PTRs (Aggregate Trial Statistics)**: Get aggregate statistics across clinical trials

## Installation

```bash
pip install gosset-sdk
```

## Quick Start

### Basic Usage

```python
from gosset_sdk import GossetClient

# Initialize (uses GOSSET_API_KEY or GOSSET_OAUTH_TOKEN from environment)
client = GossetClient()

# Classify a disease
result = client.classify_diseases("Breast Cancer")
print(result['disease_classes'])  # ['GD-01']

# Get aggregate trial statistics
stats = client.estimate_ptrs(phase=2)
print(f"Total Phase 2 trials: {stats['total_trials']}")
print(f"Success rate: {stats['average_met_endpoints_one']:.1%}")

# Clean up
client.close()
```

### Using Context Manager

```python
with GossetClient() as client:
    stats = client.estimate_ptrs(phase=3)
    print(f"Phase 3 trials: {stats['total_trials']}")
```

## Authentication

The client requires an API key or OAuth token. Set one of these environment variables:

```bash
# Option 1: API Key
export GOSSET_API_KEY='your_api_key_here'

# Option 2: OAuth Token
export GOSSET_OAUTH_TOKEN='your_oauth_token_here'
```

Or provide directly:

```python
client = GossetClient(api_key="your_api_key_here")
```

## API Methods

### `classify_diseases(disease_name, disease_desc="")`

Map a disease name to Gosset Disease (GD) classification IDs.

**Parameters:**
- `disease_name` (str): Name of the disease (e.g., "Breast Cancer")
- `disease_desc` (str, optional): Additional description for better classification

**Returns:**
```python
{
    "disease_classes": ["GD-01", "GD-02"]
}
```

**Example:**
```python
result = client.classify_diseases("Non-small cell lung cancer")
disease_classes = result['disease_classes']
print(disease_classes)  # ['GD-01']
```

### `estimate_ptrs(disease_classes=None, phase=None)`

Get aggregate trial statistics across clinical trials.

**Parameters:**
- `disease_classes` (str or list, optional): Disease class ID(s) to filter by
  - Single: `'GD-01'`
  - Multiple: `['GD-01', 'GD-02']`
- `phase` (int, optional): Clinical trial phase (1, 2, 3, or 4)

**Returns:**
```python
{
    "total_trials": 1234,
    "trials_with_endpoint_data": 980,
    "average_met_endpoints_one": 0.65,  # 65%
    "average_met_endpoints_all": 0.45,  # 45%
    "average_progressed": 0.55,  # 55%
    "average_arm_size": 125.5,
    "trials_with_comparator": 650,
    "multi_arm_trials": 320,
    "trials_with_genomics": 180,
    "trials_with_biomarkers": 150
}
```

**Examples:**

```python
# All Phase 2 trials
stats = client.estimate_ptrs(phase=2)

# Specific disease class
stats = client.estimate_ptrs(disease_classes='GD-01')

# Combine filters
stats = client.estimate_ptrs(disease_classes='GD-01', phase=2)

# Multiple disease classes
stats = client.estimate_ptrs(disease_classes=['GD-01', 'GD-02'])

# No filters (all trials)
stats = client.estimate_ptrs()
```

## Common Use Cases

### 1. Disease Classification Workflow

```python
# Step 1: Classify the disease
result = client.classify_diseases("Alzheimer's Disease")
disease_classes = result['disease_classes']

# Step 2: Get trial statistics for that disease
stats = client.estimate_ptrs(disease_classes=disease_classes, phase=3)

print(f"Phase 3 trials: {stats['total_trials']}")
print(f"Success rate: {stats['average_met_endpoints_one']:.1%}")
```

### 2. Compare Success Rates Across Phases

```python
for phase in [1, 2, 3, 4]:
    stats = client.estimate_ptrs(phase=phase)
    print(f"Phase {phase}: {stats['average_met_endpoints_one']:.1%}")
```

### 3. Analyze Multiple Disease Classes

```python
disease_classes = ['GD-01', 'GD-02', 'GD-03']

for dc in disease_classes:
    stats = client.estimate_ptrs(disease_classes=dc, phase=2)
    print(f"{dc}: {stats['total_trials']} trials, "
          f"{stats['average_met_endpoints_one']:.1%} success rate")
```

### 4. Comprehensive Disease Analysis

```python
# Classify the disease
result = client.classify_diseases("Multiple Myeloma")
disease_classes = result['disease_classes']

# Get statistics for each phase
for phase in [2, 3]:
    stats = client.estimate_ptrs(
        disease_classes=disease_classes,
        phase=phase
    )
    
    print(f"\nPhase {phase} Statistics:")
    print(f"  Total trials: {stats['total_trials']}")
    print(f"  Success rate (any endpoint): {stats['average_met_endpoints_one']:.1%}")
    print(f"  Success rate (all endpoints): {stats['average_met_endpoints_all']:.1%}")
    print(f"  Progression rate: {stats['average_progressed']:.1%}")
    print(f"  Avg arm size: {stats['average_arm_size']:.0f}")
```

## Statistics Explained

### Trial Counts
- `total_trials`: Total number of trials matching filters
- `trials_with_endpoint_data`: Trials with outcome/endpoint data available
- `trials_with_comparator`: Trials with a comparator arm
- `multi_arm_trials`: Trials with multiple treatment arms
- `trials_with_genomics`: Trials that include genomic data
- `trials_with_biomarkers`: Trials that include biomarker data

### Success Metrics (0.0 - 1.0)
- `average_met_endpoints_one`: Average proportion of trials meeting at least one primary endpoint
- `average_met_endpoints_all`: Average proportion of trials meeting all primary endpoints
- `average_progressed`: Average proportion of trials that progressed to next phase

### Other Metrics
- `average_arm_size`: Average number of participants per trial arm

## Error Handling

```python
from gosset_sdk import GossetClient
import requests

try:
    client = GossetClient()
except ValueError as e:
    print(f"Initialization error: {e}")
    # API key not found

try:
    stats = client.estimate_ptrs(phase=2)
except requests.HTTPError as e:
    print(f"API error: {e}")
    # API request failed (401, 404, 500, etc.)
except requests.RequestException as e:
    print(f"Network error: {e}")
    # Network/connection error
```

## Configuration

### Custom Base URL

```python
client = GossetClient(
    api_key="your_key",
    base_url="https://custom.api.url"
)
```

### Custom Timeout

```python
client = GossetClient(
    api_key="your_key",
    timeout=60  # seconds
)
```

### Environment Variables

```bash
# API authentication
export GOSSET_API_KEY='your_key'
# or
export GOSSET_OAUTH_TOKEN='your_token'

# Optional: Custom API URL
export GOSSET_API_URL='https://api.gosset.ai'
```

## Examples

See the `examples/` directory for complete examples:

- `examples/client_minimal.py` - Minimal usage examples
- `examples/client_demo.py` - Comprehensive demonstration

Run them:
```bash
python examples/client_minimal.py
python examples/client_demo.py
```

## Testing

Run the test suite:

```bash
# Install dev dependencies
pip install gosset-sdk[dev]

# Run tests
pytest tests/test_client.py -v
```

## Comparison with gosset-ptrs

The GossetClient provides the same functionality as the gosset-ptrs demo scripts, but as a reusable, installable library:

| gosset-ptrs | GossetClient |
|-------------|--------------|
| `classify_disease(name)` | `client.classify_diseases(name)` |
| `get_ptrs_data(disease_classes, phase)` | `client.estimate_ptrs(disease_classes, phase)` |

**Benefits of GossetClient:**
- ✅ Installable package
- ✅ Proper error handling
- ✅ Context manager support
- ✅ Type hints
- ✅ Comprehensive documentation
- ✅ Test suite

## Support

- 📧 Email: support@gosset.ai
- 🌐 Website: [gosset.ai](https://gosset.ai)
- 📖 Docs: [main.gosset-docs.pages.dev](https://main.gosset-docs.pages.dev)

## License

MIT License - see LICENSE file for details.

