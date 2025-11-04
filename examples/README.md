# Gosset SDK Examples

This directory contains examples showing how to build AI agents with Gosset's drug database.

## Prerequisites

1. Install the SDK with agent support:
```bash
pip install gosset-sdk[agents]
```

2. Get your OAuth token:
```bash
gosset get-token
```

3. Set the token as an environment variable:
```bash
export GOSSET_OAUTH_TOKEN='your_token_here'
```

Or create a `.env` file:
```bash
GOSSET_OAUTH_TOKEN=your_oauth_token_here
```

## Available Examples

### client_minimal.py

A minimal example showing the essential GossetClient usage:
- Initialize the client
- Classify diseases
- Query aggregate trial statistics (PTRs)
- Filter by phase and disease classes

**Run it:**
```bash
python examples/client_minimal.py
```

**What it does:**
- Demonstrates disease classification API
- Shows how to query PTRs with various filters
- Quick reference for common operations

### client_demo.py

A comprehensive demonstration of the GossetClient:
- All GossetClient features with detailed output
- Error handling examples
- Context manager usage
- Multiple query patterns

**Run it:**
```bash
python examples/client_demo.py
```

**What it does:**
- Full walkthrough of disease classification
- Detailed PTRs queries with different filter combinations
- Best practices for using the client

### biotech_agent.py

A basic biotech research assistant that demonstrates:
- Connecting to Gosset MCP server
- Creating an AI agent with access to the drug database
- Running queries about drugs, trials, and targets

**Run it:**
```bash
python examples/biotech_agent.py
```

**What it does:**
- Queries EGFR inhibitors in Phase 3 clinical trials
- Shows how to integrate Gosset data with OpenAI Agents SDK
- Demonstrates proper authentication and agent configuration

## Building Your Own Agent

### Basic Pattern

```python
import asyncio
import os
from agents import Agent, Runner
from agents.mcp import MCPServerSse
from agents.model_settings import ModelSettings

async def main():
    # Connect to Gosset
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
        
        # Create your agent
        agent = Agent(
            name="Your Agent Name",
            instructions="Your agent's instructions...",
            mcp_servers=[server],
            model_settings=ModelSettings(tool_choice="auto"),
        )

        # Run queries
        result = await Runner.run(agent, "Your question here")
        print(result.final_output)

asyncio.run(main())
```

### Example Use Cases

**Drug Discovery:**
```python
"Find all antibody-drug conjugates targeting HER2"
"Show me novel mechanisms for treating Parkinson's disease"
```

**Clinical Trials:**
```python
"What Phase 2 trials for multiple sclerosis started in 2024?"
"Compare success rates of CAR-T therapies across indications"
```

**Competitive Intelligence:**
```python
"Analyze the competitive landscape for GLP-1 agonists"
"Show me Moderna's pipeline of oncology drugs"
```

**Target Analysis:**
```python
"What drugs target KRAS G12C mutation?"
"Analyze the druggability of NLRP3 inflammasome"
```

## Advanced Patterns

### Multi-Agent System

```python
class ResearchTeam:
    async def create_discovery_agent(self):
        """Agent specialized in drug discovery"""
        # Implementation...
    
    async def create_clinical_agent(self):
        """Agent specialized in clinical trials"""
        # Implementation...
    
    async def analyze_therapeutic_area(self, area: str):
        """Coordinate multiple agents for comprehensive analysis"""
        # Implementation...
```

### Custom Tool Filtering

```python
from agents.mcp import create_static_tool_filter

async with MCPServerSse(
    name="Gosset Drug Database",
    params={"url": "https://mcp.gosset.ai/sse", ...},
    tool_filter=create_static_tool_filter(
        allowed_tool_names=["find_drugs", "search", "fetch"]
    ),
) as server:
    # Your agent only has access to specified tools
```

### Error Handling

```python
from agents.exceptions import AgentException

async def robust_query(agent, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = await Runner.run(agent, query)
            return result.final_output
        except AgentException as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## Need Help?

- 📖 [Full Documentation](https://main.gosset-docs.pages.dev)
- 🤖 [Custom Agents Guide](https://main.gosset-docs.pages.dev/guide/custom-agents)
- 💬 Contact: support@gosset.ai

## Contributing

Have a great example to share? Submit a PR!

1. Fork the repository
2. Add your example to this directory
3. Update this README
4. Submit a pull request

