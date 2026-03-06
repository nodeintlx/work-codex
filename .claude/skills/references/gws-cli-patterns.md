# Google Workspace CLI (gws) — Quick Reference

This reference documents `gws` CLI patterns for common Google Workspace operations. Skills should prefer `gws` via Bash for read operations (lower token cost than MCP tools) and fall back to MCP tools for complex write operations that benefit from structured input.

## Why Use gws Instead of MCP Tools

MCP tool calls include full tool schemas in context, consuming tokens even before the call executes. A `gws` command via Bash is just a string — the token cost is the command itself plus the result. For bulk reads (listing emails, fetching calendars), this saves significant context.

**Use gws via Bash for**: listing, reading, searching, fetching
**Use MCP tools for**: drafting emails (needs approval flow), complex document edits, operations requiring structured input validation

## Authentication

gws uses OAuth credentials stored at `~/.config/gws/`. Run `gws auth status` to check current auth state. If not authenticated, Makir needs to run:

```bash
gws auth login --scopes gmail,calendar,drive,docs,sheets,contacts
```

## Common Patterns

### Gmail

```bash
# List unread emails (last 24 hours)
gws gmail users messages list --params '{"userId": "me", "q": "is:unread newer_than:1d", "maxResults": 20}'

# List unread from specific sender
gws gmail users messages list --params '{"userId": "me", "q": "is:unread from:dayo.adu@moroomafrica.com"}'

# Get a specific message (full content)
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID", "format": "full"}'

# Get message metadata only (lighter)
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID", "format": "metadata"}'

# Search emails by subject
gws gmail users messages list --params '{"userId": "me", "q": "subject:position paper"}'

# Search sent emails (for follow-up tracking)
gws gmail users messages list --params '{"userId": "me", "q": "in:sent newer_than:14d"}'

# List email threads
gws gmail users threads list --params '{"userId": "me", "q": "from:eleas.eduga@oandoenergy.com"}'

# Get full thread
gws gmail users threads get --params '{"userId": "me", "id": "THREAD_ID"}'

# List labels
gws gmail users labels list --params '{"userId": "me"}'

# Get user profile (message count, etc.)
gws gmail users getProfile --params '{"userId": "me"}'
```

### Calendar

```bash
# Get today's events (replace YYYY-MM-DD with actual date)
gws calendar events list --params '{"calendarId": "primary", "timeMin": "YYYY-MM-DDT00:00:00-05:00", "timeMax": "YYYY-MM-DDT23:59:59-05:00", "singleEvents": true, "orderBy": "startTime"}'

# Get next 7 days of events (replace START and END with YYYY-MM-DD)
gws calendar events list --params '{"calendarId": "primary", "timeMin": "START-DATET00:00:00-05:00", "timeMax": "END-DATET23:59:59-05:00", "singleEvents": true, "orderBy": "startTime"}'

# Get a specific event
gws calendar events get --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'

# List calendars
gws calendar calendarList list
```

### Drive

```bash
# List recent files
gws drive files list --params '{"pageSize": 10, "orderBy": "modifiedTime desc"}'

# Search files by name
gws drive files list --params '{"q": "name contains '\''position paper'\''", "pageSize": 10}'

# Search files in a specific folder
gws drive files list --params '{"q": "'\''FOLDER_ID'\'' in parents", "pageSize": 20}'

# Get file metadata
gws drive files get --params '{"fileId": "FILE_ID"}'

# Download file content
gws drive files get --params '{"fileId": "FILE_ID", "alt": "media"}' --output ./downloaded-file.pdf

# List shared drives
gws drive drives list

# Get account info (storage quota)
gws drive about get --params '{"fields": "user,storageQuota"}'
```

### Docs

```bash
# Get document content
gws docs documents get --params '{"documentId": "DOC_ID"}'
```

### Sheets

```bash
# Read spreadsheet values — use heredoc to avoid shell escaping issues with '!'
gws sheets spreadsheets values get --params "$(cat <<'EOF'
{"spreadsheetId": "SHEET_ID", "range": "Sheet1!A1:Z100"}
EOF
)"

# Get spreadsheet metadata (no escaping issue)
gws sheets spreadsheets get --params '{"spreadsheetId": "SHEET_ID"}'

# Create a spreadsheet (use --json for request body)
gws sheets spreadsheets create --json '{"properties": {"title": "My Spreadsheet"}}'
```

### Contacts (People API)

```bash
# List contacts
gws people people connections list --params '{"resourceName": "people/me", "personFields": "names,emailAddresses,organizations"}'

# Search contacts
gws people people searchContacts --params '{"query": "Dayo", "readMask": "names,emailAddresses,organizations"}'
```

## Output Handling

```bash
# Default output is JSON — pipe through python3 for extraction (jq not installed)
gws gmail users messages list --params '{"userId": "me", "q": "is:unread", "maxResults": 5}' | python3 -c "import sys,json; data=json.load(sys.stdin); [print(m['id']) for m in data.get('messages',[])]"

# Extract specific fields from a message
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID", "format": "metadata"}' | python3 -c "import sys,json; data=json.load(sys.stdin); print(data.get('snippet',''))"

# Table format for human-readable output
gws drive files list --params '{"pageSize": 5}' --format table

# Auto-paginate for bulk operations (outputs NDJSON — one JSON object per page)
gws gmail users messages list --params '{"userId": "me", "q": "is:unread"}' --page-all | python3 -c "
import sys, json
msgs = []
for line in sys.stdin:
    line = line.strip()
    if line:
        page = json.loads(line)
        msgs.extend(page.get('messages', []))
print(json.dumps(msgs, indent=2))
"
```

## Write Operations — Syntax Note

For write operations, use `--json` (not `--body`) to pass the request body:

```bash
# Create a spreadsheet
gws sheets spreadsheets create --json '{"properties": {"title": "Test Sheet"}}'

# Delete a file
gws drive files delete --params '{"fileId": "FILE_ID"}'
```

## Error Handling

If `gws` returns an auth error, check:
1. `gws auth status` — is auth configured?
2. Token may have expired — run `gws auth login` to refresh
3. Scope may be missing — the command will indicate which scope is needed

If `gws` is not available (not installed, auth broken), fall back to MCP tools. Always check `which gws` before attempting CLI commands in a skill.

## Token Cost Comparison

| Operation | MCP Approach | gws CLI Approach | Savings |
|-----------|-------------|-----------------|---------|
| List 20 unread emails | ~2,000 tokens (tool schema + call + result) | ~500 tokens (bash command + result) | ~75% |
| Get calendar events | ~1,500 tokens | ~400 tokens | ~73% |
| Search Drive files | ~1,800 tokens | ~450 tokens | ~75% |
| Get email thread | ~2,200 tokens | ~600 tokens | ~72% |

These are estimates. The key saving is that MCP tool schemas are loaded into context once per tool type used, while Bash commands carry no schema overhead.
