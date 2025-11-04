# Migration from gosset-ptrs to GossetClient

This guide shows how to migrate from the gosset-ptrs demo scripts to the GossetClient in gosset-sdk.

## Quick Comparison

| gosset-ptrs | GossetClient |
|-------------|--------------|
| Standalone scripts | Installable package |
| Manual HTTP requests | High-level client methods |
| `classify_disease()` function | `client.classify_diseases()` method |
| `get_ptrs_data()` function | `client.estimate_ptrs()` method |

## Side-by-Side Examples

### Authentication Setup

**gosset-ptrs:**
```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOSSET_API_KEY")
BASE_URL = os.getenv("GOSSET_API_URL", "https://api.gosset.ai")

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
```

**GossetClient:**
```python
from gosset_sdk import GossetClient

# Automatically reads GOSSET_API_KEY or GOSSET_OAUTH_TOKEN
client = GossetClient()
```

### Disease Classification

**gosset-ptrs:**
```python
def classify_disease(disease_name, disease_desc=''):
    url = f"{BASE_URL}/v2/trials/disease-class/"
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    body = {
        'disease_name': disease_name,
        'disease_desc': disease_desc
    }
    
    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response: {response.text}")
        return None
    
    return response.json()

# Usage
classification = classify_disease("Breast Cancer")
if classification:
    disease_classes = classification['disease_classes']
```

**GossetClient:**
```python
# Usage
classification = client.classify_diseases("Breast Cancer")
disease_classes = classification['disease_classes']
```

### PTRs Query

**gosset-ptrs:**
```python
def get_ptrs_data(disease_classes=None, phase=None):
    url = f"{BASE_URL}/v2/trials/ptrs/"
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    body = {}
    if disease_classes:
        if not isinstance(disease_classes, list):
            disease_classes = [disease_classes]
        body['disease_classes'] = disease_classes
    if phase:
        body['phase'] = phase
    
    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response: {response.text}")
        return None
    
    return response.json()

# Usage
stats = get_ptrs_data(disease_classes=['GD-01'], phase=2)
if stats:
    print(f"Total trials: {stats['total_trials']}")
```

**GossetClient:**
```python
# Usage - accepts both string and list
stats = client.estimate_ptrs(disease_classes='GD-01', phase=2)
print(f"Total trials: {stats['total_trials']}")
```

## Complete Migration Example

### Before (gosset-ptrs style)

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOSSET_API_KEY")
BASE_URL = "https://api.gosset.ai"

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Classify disease
response = requests.post(
    f"{BASE_URL}/v2/trials/disease-class/",
    headers=headers,
    json={'disease_name': 'Breast Cancer', 'disease_desc': ''}
)

if response.ok:
    data = response.json()
    disease_classes = data['disease_classes']
    print(f"Disease classes: {disease_classes}")

# Get PTRs
response = requests.post(
    f"{BASE_URL}/v2/trials/ptrs/",
    headers=headers,
    json={'phase': 2, 'disease_classes': disease_classes}
)

if response.ok:
    stats = response.json()
    print(f"Total trials: {stats['total_trials']}")
    print(f"Success rate: {stats['average_met_endpoints_one']:.2%}")
```

### After (GossetClient)

```python
from gosset_sdk import GossetClient

# Initialize client
client = GossetClient()

# Classify disease
data = client.classify_diseases("Breast Cancer")
disease_classes = data['disease_classes']
print(f"Disease classes: {disease_classes}")

# Get PTRs
stats = client.estimate_ptrs(disease_classes=disease_classes, phase=2)
print(f"Total trials: {stats['total_trials']}")
print(f"Success rate: {stats['average_met_endpoints_one']:.2%}")

# Clean up
client.close()
```

## Migration Checklist

- [ ] Install gosset-sdk: `pip install gosset-sdk`
- [ ] Replace imports: `from gosset_sdk import GossetClient`
- [ ] Replace function calls with client methods
- [ ] Remove manual HTTP request code
- [ ] Remove manual header setup
- [ ] Update error handling (HTTPError instead of checking response.ok)
- [ ] Use context manager for automatic cleanup (optional)

## Benefits of GossetClient

✅ **Less boilerplate**: No need to manually setup headers, URLs, or requests  
✅ **Better error handling**: Raises proper exceptions instead of returning None  
✅ **Type hints**: IDE auto-completion and type checking  
✅ **Context manager**: Automatic resource cleanup  
✅ **Session reuse**: Better performance through connection pooling  
✅ **Flexible parameters**: Accepts both strings and lists for disease_classes  
✅ **Installable**: Use across multiple projects without copying code  
✅ **Tested**: Includes comprehensive test suite  
✅ **Documented**: Inline documentation and comprehensive guides

## Error Handling Improvements

**gosset-ptrs:**
```python
response = requests.post(url, headers=headers, json=body)

if response.status_code != 200:
    print(f"Error: Received status code {response.status_code}")
    print(f"Response: {response.text}")
    return None

return response.json()
```

**GossetClient:**
```python
try:
    stats = client.estimate_ptrs(phase=2)
    # Handle success
except requests.HTTPError as e:
    # Handle API errors (4xx, 5xx)
    print(f"API error: {e}")
except requests.RequestException as e:
    # Handle network errors
    print(f"Network error: {e}")
```

## Context Manager Pattern

**gosset-ptrs:**
```python
# Manual cleanup not explicitly handled
```

**GossetClient:**
```python
# Automatic cleanup with context manager
with GossetClient() as client:
    stats = client.estimate_ptrs(phase=2)
    # Client session automatically closed after this block
```

## Environment Variables

Both approaches use the same environment variables:

```bash
# API Key (either works)
export GOSSET_API_KEY='your_key'
# or
export GOSSET_OAUTH_TOKEN='your_token'

# Optional: Custom API URL
export GOSSET_API_URL='https://api.gosset.ai'
```

## Need Help?

- See `examples/client_minimal.py` for a quick reference
- See `examples/client_demo.py` for a comprehensive demo
- See `CLIENT_GUIDE.md` for detailed documentation
- Contact support@gosset.ai for assistance

