# MCP Server Integrations — Active

## Current MCP Servers (5 active + 1 CLI)

### 1. Google Workspace — Dual Mode (MCP + CLI)

**MCP Server** (`workspace-mcp` — legacy, kept as fallback):
- **Tier**: `extended`
- **Services**: Gmail, Drive, Calendar, Docs, Sheets, Chat, Forms, Slides, Tasks, Contacts, Search, Apps Script
- **Auth**: OAuth via environment variables (GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET)
- **Use for**: Complex write operations (draft emails, manage drive access, export docs), structured operations requiring input validation

**CLI** (`gws` — Google Workspace CLI v0.4.4, official Google tool):
- **Installed**: 2026-03-05 via `npm install -g @googleworkspace/cli`
- **Binary**: `gws` (available in PATH)
- **Auth**: OAuth via `~/.config/gws/` (requires one-time `gws auth login`)
- **Use for**: Read operations via Bash (list emails, get calendar, search drive) — ~75% token savings vs MCP
- **Docs**: See `~/.claude/skills/references/gws-cli-patterns.md` for command patterns

**Token Efficiency Strategy**:
- Prefer `gws` CLI via Bash for all **read** operations (list, get, search)
- Use MCP tools for **write** operations (draft emails, create docs, manage permissions)
- If `gws` auth is not configured, fall back to MCP tools seamlessly
- Check `gws auth status` at session start to determine availability

**Planned migration**: Once `gws` auth is configured and stable, replace `workspace-mcp` in .mcp.json with `gws mcp -s gmail,calendar,drive,docs,sheets,contacts` for a unified Google Workspace integration.

### 2. Filesystem (`@modelcontextprotocol/server-filesystem`)
- **Scope**: ~/Work/ directory only
- **Tools**: read_file, list_directory, search_files, directory_tree

### 3. Memory (`@modelcontextprotocol/server-memory`)
- **Storage**: ~/Work/knowledge/memory.jsonl
- **Tools**: create_entities, create_relations, add_observations, delete_entities, read_graph, search_nodes, open_nodes
- **Usage**: Load at session start, save decisions/context at session end

### 4. Brave Search (`@brave/brave-search-mcp-server`)
- **Tier**: Free (2,000 queries/month)
- **Best for**: General web search, quick lookups, news, company info
- **Auth**: BRAVE_API_KEY environment variable
- **Added**: 2026-03-02

### 5. Tavily (`tavily-mcp`)
- **Best for**: Deep research, citation-quality results, synthesized answers
- **Auth**: TAVILY_API_KEY environment variable
- **Added**: 2026-03-02

## Search Strategy
- **Quick lookups** (company info, contact details, news): Use Brave Search
- **Deep research** (legal precedents, market analysis, technical topics): Use Tavily
- **Codebase/file search**: Use built-in Glob/Grep
- **Google Drive/Docs**: Prefer `gws` CLI, fall back to Google Workspace MCP tools

## Google Workspace Tool Selection Guide

| Operation | Use | Why |
|-----------|-----|-----|
| List unread emails | `gws` CLI via Bash | ~500 tokens vs ~2,000 for MCP |
| Get calendar events | `gws` CLI via Bash | ~400 tokens vs ~1,500 for MCP |
| Search Drive files | `gws` CLI via Bash | ~450 tokens vs ~1,800 for MCP |
| Draft an email | MCP `draft_gmail_message` | Needs structured input + approval flow |
| Share a Drive file | MCP `manage_drive_access` | Complex permissions model |
| Export doc to PDF | MCP `export_doc_to_pdf` | Binary output handling |
| Get doc as markdown | MCP `get_doc_as_markdown` | Structured content extraction |
| Bulk email fetch | `gws` CLI with `--page-all` | Pagination + jq filtering |

## Upgrade Path
- **Immediate**: Complete `gws auth login` to activate CLI mode
- **Next**: Replace `workspace-mcp` in .mcp.json with `gws mcp -s gmail,calendar,drive,docs,sheets,contacts`
- **Future**: Consider `gws mcp` with `-w` (workflows) and `-e` (helpers) flags for advanced operations
- **Future**: Slack MCP (if team communication needed), GitHub MCP (if code repos needed)

## Security
- All outbound actions (send email, create draft, share files, modify calendar) require Makir's approval via hooks
- `gws` CLI follows the same approval model — write commands must be reviewed before execution
- Brave Search and Tavily are read-only by nature — no outbound risk
- Memory MCP is auto-allowed for all operations
- `gws` prompt injection protection available via `--sanitize` flag (Model Armor integration)
