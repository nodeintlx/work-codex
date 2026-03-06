# MCP Server Integrations — Active

## Current MCP Servers (5 active)

### 1. Google Workspace — gws CLI in MCP Mode

**Primary** (`gws mcp` — Google's official CLI, active since 2026-03-05):
- **Binary**: `gws` v0.4.4 (installed via `npm install -g @googleworkspace/cli`)
- **MCP config**: `"command": "gws", "args": ["mcp", "-s", "gmail,calendar,drive,docs,sheets"]`
- **Auth**: OAuth via `~/.config/gws/credentials.json` (project: `claude-mac-assistant`)
- **Scopes**: gmail.modify, calendar, drive, documents, spreadsheets, contacts, cloud-platform
- **Tool naming**: Google API style — `gmail_users_messages_list`, `calendar_events_list`, `drive_files_list`, etc.

**Token Efficiency Strategy**:
- Prefer `gws` CLI via Bash for all **read** operations (list, get, search) — ~75% token savings
- Use MCP tools for **write** operations (draft emails, create docs, manage permissions)
- If `gws` auth fails, fall back to MCP tools seamlessly
- Check `gws auth status` at session start to determine availability

**Reference**: See `~/.claude/skills/references/gws-cli-patterns.md` for command patterns.

### 2. Filesystem (`@modelcontextprotocol/server-filesystem`)
- **Scope**: ~/Work/ directory only
- **Tools**: read_file, read_text_file, read_multiple_files, list_directory, list_directory_with_sizes, search_files, directory_tree, get_file_info, write_file, edit_file, create_directory, move_file

### 3. Memory (`@modelcontextprotocol/server-memory`)
- **Storage**: ~/Work/knowledge/memory.jsonl
- **Tools**: create_entities, create_relations, add_observations, delete_entities, delete_relations, delete_observations, read_graph, search_nodes, open_nodes
- **Usage**: Load at session start, save decisions/context at session end

### 4. Brave Search (`@brave/brave-search-mcp-server`)
- **Tier**: Free (2,000 queries/month)
- **Best for**: General web search, quick lookups, news, company info
- **Auth**: BRAVE_API_KEY environment variable
- **Status**: Requires API key in ~/.zshrc — if missing, use built-in WebSearch as fallback
- **Added**: 2026-03-02

### 5. Tavily (`tavily-mcp`)
- **Best for**: Deep research, citation-quality results, synthesized answers
- **Auth**: TAVILY_API_KEY environment variable
- **Status**: Requires API key in ~/.zshrc — if missing, use built-in WebSearch as fallback
- **Added**: 2026-03-02

## Search Strategy
- **Quick lookups** (company info, contact details, news): Use Brave Search (or WebSearch fallback)
- **Deep research** (legal precedents, market analysis, technical topics): Use Tavily (or WebSearch fallback)
- **Codebase/file search**: Use built-in Glob/Grep
- **Google Drive/Docs**: Prefer `gws` CLI, fall back to Google Workspace MCP tools

## Google Workspace Tool Selection Guide

| Operation | Use | Why |
|-----------|-----|-----|
| List unread emails | `gws` CLI via Bash | ~500 tokens vs ~2,000 for MCP |
| Get calendar events | `gws` CLI via Bash | ~400 tokens vs ~1,500 for MCP |
| Search Drive files | `gws` CLI via Bash | ~450 tokens vs ~1,800 for MCP |
| Draft an email | MCP `gmail_users_drafts_create` | Needs structured input + approval flow |
| Send a draft | MCP `gmail_users_drafts_send` | Requires approval hook |
| Create calendar event | MCP `calendar_events_insert` | Needs approval hook |
| Share a Drive file | MCP `drive_permissions_create` | Complex permissions model + approval |
| Delete a Drive file | MCP `drive_files_delete` | Requires approval hook |
| Get doc content | MCP `docs_documents_get` | Structured content extraction |
| Read sheet values | `gws` CLI via Bash (heredoc for ranges) | Token savings, use heredoc for `!` escaping |
| Bulk email fetch | `gws` CLI with `--page-all` | Pagination + python3 filtering |

## Tool Name Reference (gws MCP)

The gws MCP server uses Google API-style tool names. Key mappings:

| Action | Tool Name |
|--------|-----------|
| List emails | `gmail_users_messages_list` |
| Get email | `gmail_users_messages_get` |
| Send email | `gmail_users_messages_send` (DENIED) |
| Create draft | `gmail_users_drafts_create` (requires approval) |
| Send draft | `gmail_users_drafts_send` (requires approval) |
| List threads | `gmail_users_threads_list` |
| Get thread | `gmail_users_threads_get` |
| List events | `calendar_events_list` |
| Create event | `calendar_events_insert` (requires approval) |
| Update event | `calendar_events_update` (requires approval) |
| Delete event | `calendar_events_delete` (requires approval) |
| List files | `drive_files_list` |
| Get file | `drive_files_get` |
| Delete file | `drive_files_delete` (requires approval) |
| Share file | `drive_permissions_create` (requires approval) |
| Get doc | `docs_documents_get` |
| Get sheet | `sheets_spreadsheets_get` |
| Read values | `sheets_spreadsheets_values_get` |

## Upgrade Path
- **Done**: `gws` auth configured and stable, .mcp.json migrated to `gws mcp`
- **Future**: Add `-w` (workflows) and `-e` (helpers) flags for advanced operations
- **Future**: Slack MCP (if team communication needed), GitHub MCP (if code repos needed)
- **Future**: Enable `--sanitize` flag for Model Armor prompt injection protection

## Security
- All outbound actions (send email, create draft, share files, modify calendar) require Makir's approval via hooks
- `gmail_users_messages_send` is **hard-denied** in both settings.json and hooks
- Draft creation, calendar modifications, and Drive sharing all trigger approval prompts
- `gws` CLI via Bash follows the same approval model — validate-outbound.sh catches write patterns
- Brave Search and Tavily are read-only by nature — no outbound risk
- Memory MCP is auto-allowed for all operations
- `gws` prompt injection protection available via `--sanitize` flag (Model Armor integration)
