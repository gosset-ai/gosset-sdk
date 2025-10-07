#!/usr/bin/env python3
"""
Example: Building a Biotech Research Assistant with Gosset

This example demonstrates how to create an AI agent that can query
Gosset's comprehensive drug database using the OpenAI Agents SDK.

Requirements:
    pip install gosset-sdk[agents]

Usage:
    1. Get your OAuth token:
       gosset get-token
       
    2. Set the token as an environment variable:
       export GOSSET_OAUTH_TOKEN='your_token_here'
       
    3. Run the example:
       python examples/biotech_agent.py
"""
import asyncio
import os
from agents import Agent, Runner
from agents.mcp import MCPServerSse
from agents.model_settings import ModelSettings

from dotenv import load_dotenv
load_dotenv()


async def main():
    # Check if token is set
    token = os.getenv('GOSSET_OAUTH_TOKEN')
    if not token:
        print("Error: GOSSET_OAUTH_TOKEN environment variable not set.")
        print("\nTo get a token, run:")
        print("  gosset get-token")
        print("\nThen set it as an environment variable:")
        print("  export GOSSET_OAUTH_TOKEN='your_token_here'")
        return
    
    # Connect to Gosset MCP server
    print("Connecting to Gosset Drug Database...")
    async with MCPServerSse(
        name="Gosset Drug Database",
        params={
            "url": "https://mcp.gosset.ai/sse",
            "headers": {
                "Authorization": f"Bearer {token}",
            },
        },
        client_session_timeout_seconds=300.0,
        cache_tools_list=True,
    ) as server:
        
        # List available tools
        print("\nListing available tools from Gosset...\n")
        tools = await server.list_tools()
        print(f"Found {len(tools)} tools:")
        print("-" * 70)
        for tool in tools:
            print(f"  • {tool.name}")
            if tool.description:
                print(f"    {tool.description}")
        print("=" * 70)
        print()
        
        # Create an agent with access to Gosset
        agent = Agent(
            name="Biotech Research Assistant",
            instructions="""
            You are a biotech research assistant with access to Gosset's 
            comprehensive drug database. Help users with:
            - Drug discovery and competitive intelligence
            - Clinical trial analysis and market research
            - Target analysis and mechanism of action research
            - Company pipeline analysis
            
            Always provide detailed, accurate information from the database.
            """,
            mcp_servers=[server],
            model_settings=ModelSettings(tool_choice="auto"),
        )

        print("Agent ready! Querying database...\n")
        print("=" * 70)
        
        # Run example queries
        queries = [
            "Show me all assets targetting CBL-B",
            # Uncomment to try more queries:
            # "What are the top 5 most advanced drugs for Alzheimer's disease?",
            # "Find all CAR-T therapies approved in the last 2 years",
        ]
        
        for query in queries:
            print(f"Query: {query}")
            print("-" * 70)
            
            result = await asyncio.wait_for(Runner.run(agent, query), timeout=300.0)
            print(result.final_output)
            print("=" * 70)
            print()


if __name__ == "__main__":
    asyncio.run(main())

