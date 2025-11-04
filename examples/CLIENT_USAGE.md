# GossetClient Usage Guide

## Installation

```bash
pip install -e /home/ubuntu/gosset-sdk
```

## Quick Start

```python
from gosset_sdk import GossetClient

# Initialize the client with your API key
client = GossetClient(api_key="your_api_key_here")

# Or set environment variable and omit api_key parameter
# export GOSSET_API_KEY="your_api_key_here"
client = GossetClient()
```

## Authentication

The client uses API key (Bearer token) authentication. You can provide the API key in two ways:

1. **Direct parameter:**
```python
client = GossetClient(api_key="your_api_key_here")
```

2. **Environment variable:**
```bash
export GOSSET_API_KEY="your_api_key_here"
```
```python
client = GossetClient()  # Will use GOSSET_API_KEY from environment
```

## Basic Usage

### 1. Search for Trials

```python
# Search for Phase 3 trials with a comparator
trials = client.get_trials(
    phase="3",
    has_comparator=True,
    limit=10
)

print(f"Found {trials['total']} trials")
for trial in trials['results']:
    print(f"NCT ID: {trial['nct_id']}")
```

### 2. Predict Trial Success (Natural Language)

```python
# Describe your trial in natural language
result = client.predict_trial_success(
    query="""
    Analyze the success probability for a Phase 2 trial of a BRAF inhibitor
    in melanoma with 80 patients per arm, targeted therapy, has comparator,
    small molecule, and double-blind randomized design.
    """
)

print(f"Prediction: {result['ref']['meta']['prediction']}")
print(f"Probability: {result['ref']['meta']['probability']:.2%}")
print(f"Extracted parameters: {result['extracted_parameters']}")
```

### 3. Predict Trial Success (Structured Parameters)

```python
# Provide structured trial parameters
result = client.predict_trial_success_direct(
    trial_params={
        "highest_phase": 3.0,
        "avg_arm_size": 150,
        "has_comparator": True,
        "therapy_type": ["targeted"],
        "targets": ["EGFR"],
        "diseases": ["non-small cell lung cancer"],
        "modalities": ["Small molecule"],
        "masking_type": "Double Blind",
        "allocation": "Randomized"
    }
)

print(f"Prediction: {result['ref']['meta']['prediction']}")
print(f"Probability: {result['ref']['meta']['probability']:.2%}")
```

### 4. Get Available Filters

```python
# Get all available filter options
filters = client.get_filters()

print(f"Available phases: {filters['phase']}")
print(f"Available statuses: {filters['status']}")
print(f"Available masking types: {filters['masking_type']}")
```

### 5. Get Aggregate Statistics

```python
# Get aggregate statistics for Phase 3 trials
stats = client.get_ptrs_stats(phase=3)

print(f"Total trials: {stats['total_trials']}")
print(f"Success rate: {stats['average_met_endpoints_one']:.2%}")
print(f"Average arm size: {stats['average_arm_size']:.1f}")
```

### 6. Classify Disease

```python
# Classify a disease to get disease class IDs
result = client.classify_disease("Non-small cell lung cancer")
print(f"Disease classes: {result['disease_classes']}")
```

## Advanced Usage

### Using as Context Manager

```python
with GossetClient(api_key="your_api_key") as client:
    trials = client.get_trials(phase="3", limit=10)
    print(f"Found {trials['total']} trials")
# Client automatically closed after context
```

### Custom Base URL

```python
# Use a different API endpoint
client = GossetClient(
    api_key="your_api_key",
    base_url="https://api.gosset.ai",  # Production endpoint
    timeout=60  # Custom timeout in seconds
)
```

### Error Handling

```python
from gosset_sdk import GossetClient, GossetAPIError

try:
    client = GossetClient(api_key="your_api_key")
    trials = client.get_trials(phase="3")
except GossetAPIError as e:
    print(f"API error: {e}")
except ValueError as e:
    print(f"Validation error: {e}")
```

## API Methods

### `get_trials()`

Search for clinical trials with comprehensive filtering.

**Parameters:**
- `offset` (int): Number of results to skip (for pagination)
- `limit` (int): Maximum number of results to return (max 100)
- `sort_by` (str): Field to sort by (prefix with '-' for descending)
- `phase` (str): Trial phase(s), comma-separated (e.g., "2,3")
- `diseases` (str): Disease IDs, comma-separated
- `targets` (str): Target IDs, comma-separated
- `modalities` (str): Modality IDs, comma-separated
- `has_comparator` (bool): Filter by trials with/without comparator
- `combination_therapy` (bool): Filter by combination therapy trials
- `has_designations` (bool): Filter by trials with FDA designations
- `completion_date_min` (str): Minimum completion date (YYYY-MM-DD)
- `completion_date_max` (str): Maximum completion date (YYYY-MM-DD)
- And many more...

**Returns:** Dict with `results`, `total`, `offset`, `limit`, and `stats`

### `predict_trial_success()`

Predict trial success from natural language description.

**Parameters:**
- `query` (str): Natural language description of the trial
- `return_id` (bool): If True, return only reference (default: True)

**Returns:** Dict with `ref`, `extracted_parameters`, and `original_query`

### `predict_trial_success_direct()`

Predict trial success using structured parameters.

**Parameters:**
- `trial_params` (dict): Dictionary of trial parameters
- `return_id` (bool): If True, return only reference (default: True)

**Returns:** Dict with `ref` containing prediction results

### `get_filters()`

Get available filter options for trials.

**Parameters:**
- `doid` (str, optional): Disease ID to filter options by

**Returns:** Dict of available filter values

### `get_ptrs_stats()`

Get aggregate trial statistics.

**Parameters:**
- `disease_classes` (list, optional): Disease class IDs to filter by
- `phase` (int, optional): Phase number (1, 2, 3, or 4)

**Returns:** Dict with aggregate statistics

### `classify_disease()`

Classify a disease to get disease class IDs.

**Parameters:**
- `disease_name` (str): Name of the disease
- `disease_desc` (str, optional): Description of the disease

**Returns:** Dict with `disease_classes`

## Complete Example

See `client_example.py` for a complete working example that demonstrates all features.

```bash
export GOSSET_API_KEY="your_api_key_here"
python examples/client_example.py
```

## Support

For questions or issues, please contact the Gosset API team or refer to the API documentation at:
https://api-dev.gosset.ai/apidocs/

