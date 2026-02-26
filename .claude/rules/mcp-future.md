# Future MCP Integrations

## Brave Search
When Brave Search API key is available, add to ~/Work/.mcp.json:
```json
"brave-search": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-brave-search"],
  "env": {
    "BRAVE_API_KEY": "${BRAVE_API_KEY}"
  }
}
```
- Free tier: 2,000 queries/month
- Fast (<15 seconds per query)
- Good for general web search

## Tavily
When Tavily API key is available, add to ~/Work/.mcp.json:
```json
"tavily": {
  "command": "npx",
  "args": ["-y", "tavily-mcp"],
  "env": {
    "TAVILY_API_KEY": "${TAVILY_API_KEY}"
  }
}
```
- Better source quality for deep research
- Citation-quality results

## Setup Steps
1. Get API key from the respective service
2. Store in macOS Keychain: `security add-generic-password -a "claude-agent" -s "[service]-api-key" -w "[key]"`
3. Update claude-work launcher to export the new key
4. Add the server config to ~/Work/.mcp.json
5. Restart Claude Code and verify with `/mcp`
