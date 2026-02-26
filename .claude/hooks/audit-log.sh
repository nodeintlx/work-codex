#!/bin/bash
# PostToolUse hook: logs all tool usage to audit.jsonl
# Called by Claude Code after every tool invocation

LOG_DIR="$HOME/Work/.claude/logs"
LOG_FILE="$LOG_DIR/audit.jsonl"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Read tool call data from stdin
INPUT=$(cat)

# Write log entry using python3
HOOK_INPUT="$INPUT" python3 -c "
import json, os, datetime

try:
    data = json.loads(os.environ.get('HOOK_INPUT', '{}'))
    entry = {
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'tool': data.get('tool_name', 'unknown'),
        'input_preview': str(data.get('tool_input', ''))[:500]
    }
    log_file = os.path.expanduser('~/Work/.claude/logs/audit.jsonl')
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')
except:
    pass
" 2>/dev/null

# Always exit 0 — audit logging should never block tool execution
exit 0
