# Gosset SDK

Python SDK for accessing Gosset's comprehensive drug database with 100,000+ drug assets. Build powerful AI agents with programmatic access to drug discovery, clinical trial, and competitive intelligence data.

## Features

🚀 **Full programmatic control** over queries and responses  
⚡ **Access** to the complete Gosset database  
🔧 **Custom AI agents** using OpenAI Agents SDK  
🎯 **Advanced filtering** and data processing  
📊 **Easy integration** with your existing tools  
🔐 **Simple OAuth authentication**

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install

```bash
# Standard installation
pip install gosset-sdk

# With agent support (recommended)
pip install gosset-sdk[agents]
```

### Step 2: Get Token

```bash
gosset get-token
```

This will:
1. Register an OAuth client
2. Open your browser for authorization
3. Display your access token

### Step 3: Set Token & Use It

```bash
export GOSSET_OAUTH_TOKEN='your_token_here'
python examples/biotech_agent.py
```

That's it! You're ready to build AI agents with Gosset's drug database.

---

## Installation

### From PyPI

```bash
# Basic installation
pip install gosset-sdk

# With agent support (includes openai-agents)
pip install gosset-sdk[agents]

# Development installation (includes testing tools)
pip install gosset-sdk[dev]

# Everything
pip install gosset-sdk[dev,agents]
```

### From Source

```bash
# Clone the repository
git clone https://github.com/gosset/gosset-sdk.git
cd gosset-sdk

# Install in development mode
pip install -e .

# Or with agents support
pip install -e .[agents]

# Or with all development tools
pip install -e .[dev,agents]
```

### Without Installation

If you don't want to install the package, use the standalone script:

```bash
# Download the standalone script
curl -O https://raw.githubusercontent.com/gosset/gosset-sdk/main/get-token-standalone.py

# Install requests library
pip install requests

# Run it
python get-token-standalone.py

```

### Verifying Installation

Run the test script to verify everything is working:

```bash
python tests/test_install.py
```

Or check the CLI:

```bash
gosset --version
```

### Requirements

- Python 3.8 or higher
- pip
- Internet connection (for OAuth flow)

### Optional Dependencies

- `openai-agents` - For building AI agents
- `python-dotenv` - For managing environment variables
- `pytest` - For running tests (dev)
- `black` - For code formatting (dev)
- `mypy` - For type checking (dev)

---

## CLI Commands

### Get Token

Get an OAuth token for API access:

```bash
# Interactive mode (opens browser)
gosset get-token

# Quiet mode (only output token - useful for scripting)
gosset get-token --quiet

# Custom API endpoint
gosset get-token --base-url https://custom.api.url

# Get help
gosset get-token --help
```

### Version

Check the installed version:

```bash
gosset --version
```

### Help

```bash
gosset --help
```

---

## Authentication

### Environment Variables

- `GOSSET_OAUTH_TOKEN` - Your OAuth access token (required)
- `OAUTH_BASE_URL` - Custom API base URL (default: https://api.gosset.ai)

### Setting the Token

**Option 1: Temporary (current session only)**
```bash
export GOSSET_OAUTH_TOKEN='your_token_here'
```

**Option 2: Persistent (add to shell config)**
```bash
# For bash
echo "export GOSSET_OAUTH_TOKEN='your_token'" >> ~/.bashrc
source ~/.bashrc

# For zsh
echo "export GOSSET_OAUTH_TOKEN='your_token'" >> ~/.zshrc
source ~/.zshrc
```

**Option 3: Using .env Files**

Create a `.env` file in your project:

```bash
GOSSET_OAUTH_TOKEN=your_oauth_token_here
```

Then in your code:

```python
from dotenv import load_dotenv
load_dotenv()
```

### Check Token Status

```bash
echo $GOSSET_OAUTH_TOKEN
```

---

## Building an Agent

### Minimal Example

```python
import asyncio
import os
from agents import Agent, Runner
from agents.mcp import MCPServerSse

async def main():
    async with MCPServerSse(
        name="Gosset Drug Database",
        params={
            "url": "https://mcp.gosset.ai/sse",
            "headers": {"Authorization": f"Bearer {os.getenv('GOSSET_OAUTH_TOKEN')}"},
        },
        client_session_timeout_seconds=300.0
    ) as server:
        agent = Agent(
            name="Drug Researcher",
            instructions="Help with drug discovery and research",
            mcp_servers=[server],
        )
        
        result = await Runner.run(agent, "Find all EGFR inhibitors in Phase 3")
        print(result.final_output)

asyncio.run(main())
```

### Full Example with Settings

```python
import asyncio
import os
from agents import Agent, Runner
from agents.mcp import MCPServerSse
from agents.model_settings import ModelSettings

async def main():
    async with MCPServerSse(
        name="Gosset Drug Database",
        params={
            "url": "https://mcp.gosset.ai/sse",
            "headers": {
                "Authorization": f"Bearer {os.getenv('GOSSET_OAUTH_TOKEN')}",
            },
        },
        cache_tools_list=True,
    ) as server:
        
        agent = Agent(
            name="Biotech Research Assistant",
            instructions="""
            You are a biotech research assistant with access to Gosset's 
            comprehensive drug database. Help users with drug discovery,
            clinical trial analysis, and competitive intelligence.
            """,
            mcp_servers=[server],
            model_settings=ModelSettings(tool_choice="auto"),
        )

        result = await Runner.run(
            agent, 
            "Show me all EGFR inhibitors in Phase 3 clinical trials"
        )
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Competitive Analysis Agent

```python
class BiotechIntelligenceAgent:
    async def analyze_therapeutic_area(self, area: str):
        """Perform comprehensive competitive analysis"""
        async with MCPServerSse(
            name="Gosset Drug Database",
            params={
                "url": "https://mcp.gosset.ai/sse",
                "headers": {"Authorization": f"Bearer {os.getenv('GOSSET_OAUTH_TOKEN')}"},
            },
        ) as server:
            agent = Agent(
                name="Competitive Intelligence Analyst",
                instructions="""
                You are an expert competitive intelligence analyst.
                Analyze market landscapes, clinical trials, and opportunities.
                """,
                mcp_servers=[server],
            )
            
            query = f"Analyze the {area} therapeutic area comprehensively"
            result = await Runner.run(agent, query)
            return result.final_output
```

See [examples/biotech_agent.py](examples/biotech_agent.py) for more examples.

---

## API Reference

### `GossetClient`

Direct API client for programmatic access to Gosset endpoints.

```python
from gosset_sdk import GossetClient

# Initialize client (uses GOSSET_API_KEY or GOSSET_OAUTH_TOKEN from environment)
client = GossetClient()

# Or provide API key directly
client = GossetClient(api_key="your_api_key_here")

# Classify diseases
result = client.classify_diseases("Breast Cancer")
print(result['disease_classes'])  # ['GD-01']

# Get aggregate trial statistics (PTRs)
stats = client.estimate_ptrs(phase=2)
print(f"Total trials: {stats['total_trials']}")
print(f"Success rate: {stats['average_met_endpoints_one']:.2%}")

# Filter by disease class
stats = client.estimate_ptrs(disease_classes='GD-01', phase=2)

# Multiple disease classes
stats = client.estimate_ptrs(disease_classes=['GD-01', 'GD-02'])

# Use as context manager
with GossetClient() as client:
    stats = client.estimate_ptrs(phase=3)

# Clean up
client.close()
```

#### `GossetClient.__init__(api_key, base_url, timeout)`

Initialize the client.

**Parameters:**
- `api_key` (str, optional): API key or OAuth token. Uses `GOSSET_API_KEY` or `GOSSET_OAUTH_TOKEN` env vars if not provided
- `base_url` (str, optional): API base URL. Defaults to `GOSSET_API_URL` env var or `https://api.gosset.ai`
- `timeout` (int, optional): Request timeout in seconds (default: 30)

#### `client.classify_diseases(disease_name, disease_desc="")`

Classify a disease to get disease class IDs.

**Parameters:**
- `disease_name` (str): Name of the disease (e.g., 'Breast Cancer')
- `disease_desc` (str, optional): Additional description for better classification

**Returns:** Dictionary with `disease_classes` list (e.g., `['GD-01']`)

#### `client.estimate_ptrs(disease_classes=None, phase=None)`

Get aggregate trial statistics (PTRs).

**Parameters:**
- `disease_classes` (str or list, optional): Disease class ID(s) (e.g., `'GD-01'` or `['GD-01', 'GD-02']`)
- `phase` (int, optional): Clinical trial phase (1, 2, 3, or 4)

**Returns:** Dictionary with aggregate statistics:
- `total_trials`: Total number of trials
- `trials_with_endpoint_data`: Trials with endpoint/outcome data
- `average_met_endpoints_one`: Average proportion meeting at least one endpoint (0.0-1.0)
- `average_met_endpoints_all`: Average proportion meeting all endpoints (0.0-1.0)
- `average_progressed`: Average proportion that progressed to next phase (0.0-1.0)
- `average_arm_size`: Average number of participants per trial arm
- `trials_with_comparator`: Trials with a comparator arm
- `multi_arm_trials`: Trials with multiple treatment arms
- `trials_with_genomics`: Trials that include genomic data
- `trials_with_biomarkers`: Trials that include biomarker data

### `gosset_sdk.get_oauth_token()`

Get OAuth token programmatically:

```python
from gosset_sdk import get_oauth_token

token = get_oauth_token(
    base_url="https://api.gosset.ai",  # Optional: custom base URL
    quiet=False  # Optional: suppress output
)
```

**Parameters:**
- `base_url` (str, optional): Custom API base URL
- `quiet` (bool, optional): If True, suppress all output except the token

**Returns:** OAuth access token string or None if failed.

### Python Usage

```python
from gosset_sdk import GossetClient, get_oauth_token, __version__

# Get token programmatically
token = get_oauth_token(quiet=True)

# Use the client
client = GossetClient()
stats = client.estimate_ptrs(phase=2)

# Check version
print(f"Using Gosset SDK v{__version__}")
```

---

## Use Cases

### Drug Discovery

**Using GossetClient:**
```python
client = GossetClient()
# Classify a disease
result = client.classify_diseases("Non-small cell lung cancer")
disease_classes = result['disease_classes']

# Get trial statistics for that disease
stats = client.estimate_ptrs(disease_classes=disease_classes, phase=3)
print(f"Phase 3 success rate: {stats['average_met_endpoints_one']:.1%}")
```

**Using AI Agent:**
```python
"Find all antibody-drug conjugates targeting HER2"
```

### Clinical Trial Intelligence

**Using GossetClient:**
```python
client = GossetClient()
# Get Phase 2 trial statistics
stats = client.estimate_ptrs(phase=2)
print(f"Total Phase 2 trials: {stats['total_trials']}")
print(f"Average progression rate: {stats['average_progressed']:.1%}")
```

**Using AI Agent:**
```python
"What Phase 2 trials for multiple sclerosis started in 2024?"
```

### Competitive Analysis

**Using GossetClient:**
```python
client = GossetClient()
# Compare success rates across disease classes
for disease_class in ['GD-01', 'GD-02', 'GD-03']:
    stats = client.estimate_ptrs(disease_classes=disease_class, phase=2)
    print(f"{disease_class}: {stats['average_met_endpoints_one']:.1%}")
```

**Using AI Agent:**
```python
"Analyze the competitive landscape for GLP-1 agonists"
```

### Target Validation

**Using AI Agent:**
```python
"What drugs target KRAS G12C mutation?"
```

### Market Research

**Using GossetClient:**
```python
client = GossetClient()
# Analyze rare disease space
rare_disease_classes = ['GD-15', 'GD-16']  # Example rare disease classes
stats = client.estimate_ptrs(disease_classes=rare_disease_classes)
print(f"Total trials in rare diseases: {stats['total_trials']}")
```

**Using AI Agent:**
```python
"Identify opportunities in the rare disease space"
```

---

## Troubleshooting

### Command Not Found: "gosset: command not found"

**Solution 1: Add pip install location to PATH**
```bash
export PATH="$HOME/.local/bin:$PATH"

# Make it permanent
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Solution 2: Use python -m**
```bash
python -m gosset_sdk.cli get-token
```

**Solution 3: Check installation**
```bash
pip show gosset-sdk
which gosset
```

### Import Errors: "No module named 'agents'"

If you get import errors when running examples:

```bash
# Install with agents support
pip install gosset-sdk[agents]

# Or install dependencies manually
pip install openai-agents python-dotenv
```

### Port Already in Use: "Address already in use"

The OAuth callback uses port 8765. If it's already in use:

```bash
# Check what's using the port
lsof -i :8765

# Kill the process
kill -9 <PID>

# Or wait a moment and try again
```

### Token Not Set

```bash
# Check if token is set
echo $GOSSET_OAUTH_TOKEN

# If empty, set it
export GOSSET_OAUTH_TOKEN='your_token'

# Make it persistent
echo "export GOSSET_OAUTH_TOKEN='your_token'" >> ~/.bashrc
source ~/.bashrc
```

### Installation Issues

```bash
# Update pip
pip install --upgrade pip

# Clear pip cache
pip cache purge

# Reinstall
pip uninstall gosset-sdk
pip install gosset-sdk[agents]
```

### Browser Doesn't Open During OAuth

If the browser doesn't open automatically:

1. Look for the URL in the terminal output
2. Copy and paste it into your browser manually
3. Complete the authorization
4. The token will be displayed in the terminal

---

## Supported Frameworks

Gosset MCP server works with any MCP-compatible framework:

- ✅ **OpenAI Agents SDK** (Recommended)
- ✅ **Custom MCP implementations**
- ✅ **LangChain with MCP support**
- ✅ **AutoGen with MCP integration**
- ✅ **Any framework supporting MCP protocol**

---

## Documentation

- 📖 [Full Documentation](https://main.gosset-docs.pages.dev)
- 🚀 [Quick Start Guide](https://main.gosset-docs.pages.dev/guide/quick-start)
- 🤖 [Custom Agents Guide](https://main.gosset-docs.pages.dev/guide/custom-agents)
- 💡 [Usage Examples](https://main.gosset-docs.pages.dev/guide/examples)

---

## Support

- 📧 Email: support@gosset.ai
- 🌐 Website: [gosset.ai](https://gosset.ai)
- 📖 Docs: [main.gosset-docs.pages.dev](https://main.gosset-docs.pages.dev)

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Changelog

### v0.1.0 (2024)
- Initial release
- OAuth authentication support
- CLI commands (`gosset get-token`)
- OpenAI Agents SDK integration
- Comprehensive examples
- Standalone token script

---

**Ready to build? Start with `gosset get-token` 🚀**
