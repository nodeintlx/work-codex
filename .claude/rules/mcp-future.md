# Future MCP Integrations — Candidates

## Already Activated (2026-03-02 — 2026-03-05)
- Brave Search — LIVE (2026-03-02)
- Tavily — LIVE (2026-03-02)
- Google Workspace extended tier — LIVE (2026-03-02)
- Google Workspace CLI (`gws` v0.4.4) — INSTALLED, pending auth (2026-03-05)

## Pending: Complete gws Auth Setup

Run these commands to activate the `gws` CLI:

```bash
# Step 1: Login with required scopes
gws auth login --scopes gmail,calendar,drive,docs,sheets,contacts

# Step 2: Verify auth works
gws auth status
gws gmail users messages list --params '{"userId": "me", "q": "is:unread", "maxResults": 3}'
```

Once auth is confirmed working, replace the workspace-mcp in .mcp.json:

```json
"google-workspace": {
  "command": "gws",
  "args": ["mcp", "-s", "gmail,calendar,drive,docs,sheets,contacts"]
}
```

This replaces the `uvx workspace-mcp --tool-tier extended` server with Google's official CLI in MCP mode, giving:
- Automatic API updates (via Google Discovery Service)
- Prompt injection protection (Model Armor `--sanitize` flag)
- Same MCP protocol, but backed by canonical API definitions

## Potential Future Additions

### Slack MCP
If NRG Bloom or Coldstorm adopts Slack for team communication:
```json
"slack": {
  "command": "npx",
  "args": ["-y", "@anthropic/mcp-server-slack"],
  "env": {
    "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
  }
}
```

### GitHub MCP
If code repository management is needed:
```json
"github": {
  "command": "npx",
  "args": ["-y", "@anthropic/mcp-server-github"],
  "env": {
    "GITHUB_TOKEN": "${GITHUB_TOKEN}"
  }
}
```

### gws Workflows + Helpers
After `gws` is stable, add workflow and helper tools for advanced operations:
```json
"google-workspace": {
  "command": "gws",
  "args": ["mcp", "-s", "gmail,calendar,drive,docs,sheets,contacts", "-w", "-e"]
}
```
- `-w`: Exposes pre-built workflow tools (multi-step operations)
- `-e`: Exposes service-specific helper tools (smart search, content extraction)
