# Future MCP Integrations — Candidates

## Already Activated (2026-03-02)
- Brave Search — LIVE
- Tavily — LIVE
- Google Workspace extended tier — LIVE

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

### Google Workspace → Complete Tier
Upgrade from `extended` to `complete` if needed:
- Document comments (manage_document_comment) — useful for reviewing shared docs with Dayo
- Batch Gmail label operations — useful for large inbox processing
- Advanced Docs structure tools — tables, images, headers
- Change `--tool-tier extended` to `--tool-tier complete` in .mcp.json
