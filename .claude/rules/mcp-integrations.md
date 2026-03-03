# MCP Server Integrations — Active

## Current MCP Servers (5 active)

### 1. Google Workspace (`workspace-mcp`)
- **Tier**: `extended` (upgraded from `core` on 2026-03-02)
- **Services**: Gmail, Drive, Calendar, Docs, Sheets, Chat, Forms, Slides, Tasks, Contacts, Search, Apps Script
- **Key extended-tier tools**: `draft_gmail_message`, `get_gmail_thread_content`, `get_gmail_attachment_content`, `manage_drive_access`, `export_doc_to_pdf`, `get_doc_as_markdown`, `query_freebusy`
- **Auth**: OAuth via environment variables (GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET)

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
- **Google Drive/Docs**: Use Google Workspace MCP tools

## Upgrade Path
- Google Workspace `complete` tier available if needed (adds document comments, batch operations, admin tools)
- Consider adding: Slack MCP (if team communication needed), GitHub MCP (if code repos needed)

## Security
- All outbound actions (send email, create draft, share files, modify calendar) require Makir's approval via hooks
- Brave Search and Tavily are read-only by nature — no outbound risk
- Memory MCP is auto-allowed for all operations
