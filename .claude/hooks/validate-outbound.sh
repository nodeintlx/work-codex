#!/bin/bash
# PreToolUse hook: validates tool calls before execution
# Blocks destructive commands and forces confirmation on outbound actions
# Updated 2026-03-05: Aligned with gws MCP tool names (gmail_users_*, calendar_events_*, drive_*)

# Read tool call data from stdin into variable
INPUT=$(cat)

# Pass via env var to python3 for safe JSON parsing
RESULT=$(HOOK_INPUT="$INPUT" python3 -c "
import json, sys, os

try:
    data = json.loads(os.environ.get('HOOK_INPUT', '{}'))
except:
    sys.exit(0)

tool_name = data.get('tool_name', '')
tool_input = data.get('tool_input', {})

# --- Block destructive bash commands ---
if tool_name == 'Bash':
    command = tool_input.get('command', '')
    blocked_patterns = [
        'rm -rf /',
        'rm -rf ~',
        'rm -rf \$HOME',
        'sudo ',
        'chmod 777',
        'curl | sh',
        'curl | bash',
        'wget | sh',
        'wget | bash',
        'mkfs.',
        'dd if=',
        '> /dev/',
    ]
    for pattern in blocked_patterns:
        if pattern in command:
            print(json.dumps({
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'deny',
                    'permissionDecisionReason': f\"Blocked: destructive command pattern detected\"
                }
            }))
            sys.exit(0)

# --- Block access to credential files ---
if tool_name in ('Read', 'Edit', 'Write'):
    file_path = tool_input.get('file_path', '')
    blocked_paths = [
        '/.ssh/', '/.aws/', '/.gnupg/',
        '.env', 'credentials.json', 'token.json',
        '/Confidential/', '/Legal/',
    ]
    for pattern in blocked_paths:
        if pattern in file_path:
            print(json.dumps({
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'deny',
                    'permissionDecisionReason': f\"Blocked: access to protected path\"
                }
            }))
            sys.exit(0)

# --- Force confirmation on MCP outbound actions (gws MCP tool names) ---
outbound_patterns = [
    # Gmail write operations
    'gmail_users_messages_send',
    'gmail_users_drafts_create',
    'gmail_users_drafts_update',
    'gmail_users_drafts_send',
    'gmail_users_messages_modify',
    'gmail_users_messages_trash',
    'gmail_users_messages_delete',
    'gmail_users_messages_batchDelete',
    'gmail_users_messages_batchModify',
    'gmail_users_messages_import',
    'gmail_users_messages_insert',
    'gmail_users_labels_create',
    'gmail_users_labels_update',
    'gmail_users_labels_delete',
    'gmail_users_settings_filters_create',
    'gmail_users_settings_filters_delete',
    # Calendar write operations
    'calendar_events_insert',
    'calendar_events_update',
    'calendar_events_delete',
    'calendar_events_move',
    # Drive write operations
    'drive_permissions_create',
    'drive_permissions_update',
    'drive_permissions_delete',
    'drive_files_delete',
    'drive_files_update',
    'drive_files_create',
    # Docs write operations
    'docs_documents_batchUpdate',
    'docs_documents_create',
    # Sheets write operations
    'sheets_spreadsheets_batchUpdate',
    'sheets_spreadsheets_values_update',
    'sheets_spreadsheets_values_append',
    'sheets_spreadsheets_values_clear',
    'sheets_spreadsheets_values_batchUpdate',
    'sheets_spreadsheets_values_batchClear',
    # Legacy tool names (workspace-mcp fallback)
    'send_gmail_message',
    'draft_gmail_message',
    'gmail_create_draft',
    'manage_event',
    'calendar_create_event',
    'manage_drive_access',
    'set_drive_file_permissions',
    'modify_gmail_message_labels',
    'manage_gmail_filter',
]

for pattern in outbound_patterns:
    if pattern in tool_name:
        print(json.dumps({
            'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'permissionDecision': 'ask',
                'permissionDecisionReason': \"Outbound action requires Makir's approval\"
            }
        }))
        sys.exit(0)

# Allow everything else
sys.exit(0)
" 2>/dev/null)

# Output the result if any
if [ -n "$RESULT" ]; then
    echo "$RESULT"
fi

exit 0
