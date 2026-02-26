#!/bin/bash
# PreToolUse hook: validates tool calls before execution
# Blocks destructive commands and forces confirmation on outbound actions

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

# --- Force confirmation on MCP outbound actions ---
if 'gmail_send' in tool_name or 'gmail_create_draft' in tool_name or 'calendar_create_event' in tool_name or 'send_message' in tool_name:
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
