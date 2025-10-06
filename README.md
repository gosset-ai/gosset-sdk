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
from gosset_sdk import get_oauth_token, __version__

# Get token programmatically
token = get_oauth_token(quiet=True)

# Check version
print(f"Using Gosset SDK v{__version__}")
```

---

## Use Cases

### Drug Discovery
```python
"Find all antibody-drug conjugates targeting HER2"
```

### Clinical Trial Intelligence
```python
"What Phase 2 trials for multiple sclerosis started in 2024?"
```

### Competitive Analysis
```python
"Analyze the competitive landscape for GLP-1 agonists"
```

### Target Validation
```python
"What drugs target KRAS G12C mutation?"
```

### Market Research
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
