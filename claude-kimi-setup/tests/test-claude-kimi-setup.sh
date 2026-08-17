#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C
export LANG=C

readonly ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
readonly TEST_DIR="$(mktemp -d /private/tmp/claude-kimi-core.XXXXXX)"
readonly ESCAPE_HOME="$(mktemp -d /private/tmp/not-claude-kimi.XXXXXX)"
readonly CHILD_ESCAPE_HOME="$(mktemp -d /private/tmp/not-claude-kimi-child.XXXXXX)"
readonly SYMLINK_ROOT="$TEST_DIR/symlink-root"
readonly NESTED_ROOT="$TEST_DIR/nested-root"
readonly KEYFAIL_HOME="$TEST_DIR/keyfail-home"
readonly ADDKEY_HOME="$TEST_DIR/addkey-home"
readonly HELPER_UNDER_TEST="$TEST_DIR/helper-sandbox/fireworks-key-helper"

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

pass() {
  printf 'PASS: %s\n' "$*"
}

cleanup() {
  set +e
  [[ ! -L "$NESTED_ROOT/.local" ]] || rm -f "$NESTED_ROOT/.local"
  [[ ! -L "$NESTED_ROOT/.claude-kimi" ]] || rm -f "$NESTED_ROOT/.claude-kimi"
  rm -f \
    "$TEST_DIR/fake-security" \
    "$HELPER_UNDER_TEST" \
    "$TEST_DIR/fake-claude" \
    "$TEST_DIR/helper.out" \
    "$TEST_DIR/helper.err" \
    "$TEST_DIR/claude.args" \
    "$TEST_DIR/config/settings.json" \
    "$TEST_DIR/install.out" \
    "$TEST_DIR/install.err" \
    "$TEST_DIR/uninstall.out" \
    "$TEST_DIR/uninstall.err" \
    "$TEST_DIR/security.calls" \
    "$TEST_DIR/security.state" \
    "$TEST_DIR/partial.settings.hash" \
    "$TEST_DIR/partial.helper.hash" \
    "$TEST_DIR/partial.launcher.hash" \
    "$TEST_DIR/traversal-backup/settings.json" \
    "$TEST_DIR/traversal-backup/fireworks-key-helper" \
    "$TEST_DIR/traversal-backup/claude-kimi" \
    "$TEST_DIR/traversal-backup/ownership-marker" \
    "$TEST_DIR/install-home/.local/bin/kimi" \
    "$TEST_DIR/install-home/.local/bin/claude-kimi" \
    "$TEST_DIR/install-home/.claude-kimi/settings.json" \
    "$TEST_DIR/install-home/.claude-kimi/bin/fireworks-key-helper" \
    "$TEST_DIR/install-home/.claude-kimi/.claude-kimi-setup-owned" \
    "$TEST_DIR/install-home/.claude-kimi/backups/test-backup/settings.json" \
    "$TEST_DIR/install-home/.claude-kimi/backups/test-backup/fireworks-key-helper" \
    "$TEST_DIR/install-home/.claude-kimi/backups/test-backup/claude-kimi" \
    "$TEST_DIR/install-home/.claude-kimi/backups/test-backup/ownership-marker" \
    "$TEST_DIR/install-home/.claude-kimi/backups/rollback-backup/settings.json" \
    "$TEST_DIR/install-home/.claude-kimi/backups/rollback-backup/fireworks-key-helper" \
    "$TEST_DIR/install-home/.claude-kimi/backups/rollback-backup/claude-kimi" \
    "$TEST_DIR/install-home/.claude-kimi/backups/rollback-backup/ownership-marker" \
    "$TEST_DIR/collision-home/.local/bin/claude-kimi" \
    "$KEYFAIL_HOME/.local/bin/claude-kimi" \
    "$KEYFAIL_HOME/.claude-kimi/settings.json" \
    "$KEYFAIL_HOME/.claude-kimi/bin/fireworks-key-helper" \
    "$KEYFAIL_HOME/.claude-kimi/.claude-kimi-setup-owned" \
    "$ADDKEY_HOME/.local/bin/claude-kimi" \
    "$ADDKEY_HOME/.claude-kimi/settings.json" \
    "$ADDKEY_HOME/.claude-kimi/bin/fireworks-key-helper" \
    "$ADDKEY_HOME/.claude-kimi/.claude-kimi-setup-owned" \
    "$NESTED_ROOT/.local/bin/claude-kimi" \
    "$NESTED_ROOT/.claude-kimi/settings.json" \
    "$NESTED_ROOT/.claude-kimi/bin/fireworks-key-helper" \
    "$NESTED_ROOT/.claude-kimi/.claude-kimi-setup-owned" \
    "$CHILD_ESCAPE_HOME/bin/claude-kimi" \
    "$CHILD_ESCAPE_HOME/settings.json" \
    "$CHILD_ESCAPE_HOME/bin/fireworks-key-helper" \
    "$CHILD_ESCAPE_HOME/.claude-kimi-setup-owned" \
    "$ESCAPE_HOME/.local/bin/claude-kimi" \
    "$ESCAPE_HOME/.claude-kimi/settings.json" \
    "$ESCAPE_HOME/.claude-kimi/bin/fireworks-key-helper" \
    "$ESCAPE_HOME/.claude-kimi/.claude-kimi-setup-owned" \
    "$SYMLINK_ROOT"
  rmdir \
    "$TEST_DIR/traversal-backup" \
    "$TEST_DIR/install-home/.claude-kimi/backups/rollback-backup" \
    "$TEST_DIR/install-home/.claude-kimi/backups/test-backup" \
    "$TEST_DIR/install-home/.claude-kimi/backups" \
    "$TEST_DIR/install-home/.claude-kimi/bin" \
    "$TEST_DIR/install-home/.claude-kimi" \
    "$TEST_DIR/install-home/.local/bin" \
    "$TEST_DIR/install-home/.local" \
    "$TEST_DIR/install-home" \
    "$TEST_DIR/collision-home/.local/bin" \
    "$TEST_DIR/collision-home/.local" \
    "$TEST_DIR/collision-home" \
    "$KEYFAIL_HOME/.claude-kimi/bin" \
    "$KEYFAIL_HOME/.claude-kimi" \
    "$KEYFAIL_HOME/.local/bin" \
    "$KEYFAIL_HOME/.local" \
    "$KEYFAIL_HOME" \
    "$ADDKEY_HOME/.claude-kimi/bin" \
    "$ADDKEY_HOME/.claude-kimi" \
    "$ADDKEY_HOME/.local/bin" \
    "$ADDKEY_HOME/.local" \
    "$ADDKEY_HOME" \
    "$TEST_DIR/helper-sandbox" \
    "$NESTED_ROOT/.claude-kimi/bin" \
    "$NESTED_ROOT/.claude-kimi" \
    "$NESTED_ROOT/.local/bin" \
    "$NESTED_ROOT/.local" \
    "$NESTED_ROOT" \
    "$CHILD_ESCAPE_HOME/bin" \
    "$CHILD_ESCAPE_HOME" \
    "$ESCAPE_HOME/.claude-kimi/bin" \
    "$ESCAPE_HOME/.claude-kimi" \
    "$ESCAPE_HOME/.local/bin" \
    "$ESCAPE_HOME/.local" \
    "$ESCAPE_HOME" \
    "$TEST_DIR/config" \
    "$TEST_DIR" 2>/dev/null
}
trap cleanup EXIT

for script in claude-kimi fireworks-key-helper; do
  [[ -f "$ROOT_DIR/$script" ]] || fail "$script is missing"
  bash -n "$ROOT_DIR/$script" || fail "$script has invalid shell syntax"
done
pass 'core shell syntax'

[[ -f "$ROOT_DIR/settings.json" ]] || fail 'settings.json is missing'
node - "$ROOT_DIR/settings.json" <<'NODE'
const fs = require('fs');
const settings = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const router = 'accounts/fireworks/routers/kimi-k3-fast';
const expected = [
  'ANTHROPIC_MODEL',
  'ANTHROPIC_SMALL_FAST_MODEL',
  'ANTHROPIC_DEFAULT_OPUS_MODEL',
  'ANTHROPIC_DEFAULT_SONNET_MODEL',
  'ANTHROPIC_DEFAULT_HAIKU_MODEL',
  'ANTHROPIC_DEFAULT_FABLE_MODEL',
  'CLAUDE_CODE_SUBAGENT_MODEL'
];
if (settings.model !== router) throw new Error('main model mismatch');
if (settings.apiKeyHelper !== '~/.claude-kimi/bin/fireworks-key-helper') {
  throw new Error('apiKeyHelper mismatch');
}
if (settings.env.ANTHROPIC_BASE_URL !== 'https://api.fireworks.ai/inference') {
  throw new Error('base URL mismatch');
}
for (const key of expected) {
  if (settings.env[key] !== router) throw new Error(`${key} mismatch`);
}
if (JSON.stringify(settings).includes('X-Fireworks-Api-Key')) {
  throw new Error('a secret-bearing header must not be stored');
}
NODE
pass 'settings route every model slot to Kimi K3'

cat > "$TEST_DIR/fake-security" <<'FAKE_SECURITY'
#!/usr/bin/env bash
set -euo pipefail

printf '%s\n' "$*" >> "${FAKE_SECURITY_CALLS:-/dev/null}"
case "${1-}:${FAKE_SECURITY_MODE:-valid}" in
  find-generic-password:valid) printf '%s\n' 'fw_fixture' ;;
  find-generic-password:wrong) printf '%s\n' 'wrong_fixture' ;;
  find-generic-password:missing) exit 44 ;;
  find-generic-password:stateful)
    [[ -f "${FAKE_SECURITY_STATE:?}" ]] || exit 44
    printf '%s\n' 'fw_fixture'
    ;;
  add-generic-password:stateful)
    last_argument=''
    for last_argument in "$@"; do :; done
    [[ "$last_argument" == '-w' ]] || exit 65
    printf '%s\n' 'present' > "${FAKE_SECURITY_STATE:?}"
    ;;
  delete-generic-password:stateful)
    rm -f "${FAKE_SECURITY_STATE:?}"
    ;;
  delete-generic-password:delete_ok) exit 0 ;;
  delete-generic-password:delete_missing) exit 44 ;;
  delete-generic-password:delete_error) exit 51 ;;
  *) exit 64 ;;
esac
FAKE_SECURITY
chmod 0700 "$TEST_DIR/fake-security"
mkdir -p "$TEST_DIR/helper-sandbox"
cp "$ROOT_DIR/fireworks-key-helper" "$HELPER_UNDER_TEST"
chmod 0700 "$HELPER_UNDER_TEST"

if CLAUDE_KIMI_TEST_SECURITY_BIN="$TEST_DIR/fake-security" \
  "$ROOT_DIR/fireworks-key-helper" >"$TEST_DIR/helper.out" 2>"$TEST_DIR/helper.err"; then
  fail 'live helper location accepted the Keychain test seam'
fi
pass 'live helper location rejects the Keychain test seam'

helper_output="$(
  CLAUDE_KIMI_SECURITY_BIN="$TEST_DIR/fake-security" \
  CLAUDE_KIMI_TEST_SECURITY_BIN="$TEST_DIR/fake-security" \
    "$HELPER_UNDER_TEST"
)"
[[ "$helper_output" == 'fw_fixture' ]] || fail 'helper did not return the valid fixture'
pass 'key helper returns a valid standard Fireworks key'

if FAKE_SECURITY_MODE=wrong \
  CLAUDE_KIMI_SECURITY_BIN="$TEST_DIR/fake-security" \
  CLAUDE_KIMI_TEST_SECURITY_BIN="$TEST_DIR/fake-security" \
  "$HELPER_UNDER_TEST" >"$TEST_DIR/helper.out" 2>"$TEST_DIR/helper.err"; then
  fail 'helper accepted a wrong key prefix'
fi
[[ ! -s "$TEST_DIR/helper.out" ]] || fail 'wrong-prefix helper call wrote to stdout'
if grep -F 'wrong_fixture' "$TEST_DIR/helper.err" >/dev/null; then
  fail 'wrong-prefix helper call exposed the fixture'
fi
pass 'key helper rejects a wrong prefix without exposure'

if FAKE_SECURITY_MODE=missing \
  CLAUDE_KIMI_SECURITY_BIN="$TEST_DIR/fake-security" \
  CLAUDE_KIMI_TEST_SECURITY_BIN="$TEST_DIR/fake-security" \
  "$HELPER_UNDER_TEST" >"$TEST_DIR/helper.out" 2>"$TEST_DIR/helper.err"; then
  fail 'helper accepted a missing Keychain item'
fi
[[ ! -s "$TEST_DIR/helper.out" ]] || fail 'missing-key helper call wrote to stdout'
pass 'key helper rejects a missing Keychain item'

: > "$TEST_DIR/security.calls"
CLAUDE_KIMI_KEYCHAIN_ACCOUNT='redirected-account' \
CLAUDE_KIMI_TEST_SECURITY_BIN="$TEST_DIR/fake-security" \
FAKE_SECURITY_CALLS="$TEST_DIR/security.calls" \
  "$HELPER_UNDER_TEST" >"$TEST_DIR/helper.out"
if grep -F 'redirected-account' "$TEST_DIR/security.calls" >/dev/null; then
  fail 'key helper accepted a redirected Keychain account'
fi
pass 'key helper fixes Keychain lookup to the current user'

if grep -F 'CLAUDE_KIMI_SECURITY_BIN' "$ROOT_DIR/fireworks-key-helper" >/dev/null; then
  fail 'key helper still accepts the legacy live security override'
fi
pass 'key helper ignores the legacy live security override'

cat > "$TEST_DIR/fake-claude" <<'FAKE_CLAUDE'
#!/usr/bin/env bash
set -euo pipefail

[[ "${CLAUDE_CONFIG_DIR:-}" == "$EXPECTED_CLAUDE_CONFIG_DIR" ]] || {
  printf 'wrong CLAUDE_CONFIG_DIR\n' >&2
  exit 90
}

for variable_name in \
  ANTHROPIC_API_KEY \
  ANTHROPIC_AUTH_TOKEN \
  ANTHROPIC_CUSTOM_HEADERS \
  ANTHROPIC_BASE_URL \
  ANTHROPIC_BEDROCK_BASE_URL \
  ANTHROPIC_VERTEX_BASE_URL \
  ANTHROPIC_MODEL \
  ANTHROPIC_SMALL_FAST_MODEL \
  ANTHROPIC_DEFAULT_OPUS_MODEL \
  ANTHROPIC_DEFAULT_SONNET_MODEL \
  ANTHROPIC_DEFAULT_HAIKU_MODEL \
  ANTHROPIC_DEFAULT_FABLE_MODEL \
  CLAUDE_CODE_SUBAGENT_MODEL \
  CLAUDE_CODE_OAUTH_TOKEN \
  CLAUDE_CODE_USE_BEDROCK \
  CLAUDE_CODE_USE_VERTEX \
  CLAUDE_CODE_USE_FOUNDRY \
  CLAUDE_KIMI_SECURITY_BIN \
  CLAUDE_KIMI_TEST_SECURITY_BIN \
  CLAUDE_KIMI_KEYCHAIN_ACCOUNT; do
  if printenv "$variable_name" >/dev/null 2>&1; then
    printf 'provider variable leaked: %s\n' "$variable_name" >&2
    exit 91
  fi
done

printf '%s\n' "$@" > "$FAKE_CLAUDE_OUTPUT"
FAKE_CLAUDE
chmod 0700 "$TEST_DIR/fake-claude"

mkdir -p "$TEST_DIR/config"
cp "$ROOT_DIR/settings.json" "$TEST_DIR/config/settings.json"

ANTHROPIC_API_KEY='anthropic_fixture' \
ANTHROPIC_AUTH_TOKEN='auth_fixture' \
ANTHROPIC_CUSTOM_HEADERS='header_fixture' \
ANTHROPIC_BASE_URL='provider_fixture' \
ANTHROPIC_BEDROCK_BASE_URL='bedrock_fixture' \
ANTHROPIC_VERTEX_BASE_URL='vertex_fixture' \
ANTHROPIC_MODEL='model_fixture' \
ANTHROPIC_SMALL_FAST_MODEL='small_fixture' \
ANTHROPIC_DEFAULT_OPUS_MODEL='opus_fixture' \
ANTHROPIC_DEFAULT_SONNET_MODEL='sonnet_fixture' \
ANTHROPIC_DEFAULT_HAIKU_MODEL='haiku_fixture' \
ANTHROPIC_DEFAULT_FABLE_MODEL='fable_fixture' \
CLAUDE_CODE_SUBAGENT_MODEL='subagent_fixture' \
CLAUDE_CODE_OAUTH_TOKEN='oauth_fixture' \
CLAUDE_CODE_USE_BEDROCK=1 \
CLAUDE_CODE_USE_VERTEX=1 \
CLAUDE_CODE_USE_FOUNDRY=1 \
CLAUDE_KIMI_SECURITY_BIN="$TEST_DIR/fake-security" \
CLAUDE_KIMI_TEST_SECURITY_BIN="$TEST_DIR/fake-security" \
CLAUDE_KIMI_KEYCHAIN_ACCOUNT='redirected-account' \
CLAUDE_KIMI_CONFIG_DIR="$TEST_DIR/config" \
CLAUDE_KIMI_CLAUDE_BIN="$TEST_DIR/fake-claude" \
EXPECTED_CLAUDE_CONFIG_DIR="$TEST_DIR/config" \
FAKE_CLAUDE_OUTPUT="$TEST_DIR/claude.args" \
  "$ROOT_DIR/claude-kimi" alpha 'two words'

[[ "$(sed -n '1p' "$TEST_DIR/claude.args")" == '--settings' ]] || fail 'launcher omitted --settings'
[[ "$(sed -n '2p' "$TEST_DIR/claude.args")" == "$TEST_DIR/config/settings.json" ]] || fail 'launcher used the wrong settings path'
[[ "$(sed -n '3p' "$TEST_DIR/claude.args")" == 'alpha' ]] || fail 'launcher changed the first argument'
[[ "$(sed -n '4p' "$TEST_DIR/claude.args")" == 'two words' ]] || fail 'launcher changed the quoted argument'
[[ "$(wc -l < "$TEST_DIR/claude.args" | tr -d ' ')" == '4' ]] || fail 'launcher added unexpected arguments'
pass 'launcher isolates provider state and forwards arguments'

[[ -f "$ROOT_DIR/install.sh" ]] || fail 'install.sh is missing'
[[ -f "$ROOT_DIR/uninstall.sh" ]] || fail 'uninstall.sh is missing'
bash -n "$ROOT_DIR/install.sh" || fail 'install.sh has invalid shell syntax'
bash -n "$ROOT_DIR/uninstall.sh" || fail 'uninstall.sh has invalid shell syntax'
pass 'installation shell syntax'

ln -s "$ESCAPE_HOME" "$SYMLINK_ROOT"
if CLAUDE_KIMI_INSTALL_ROOT="$SYMLINK_ROOT" \
  CLAUDE_KIMI_SKIP_KEYCHAIN=1 \
  "$ROOT_DIR/install.sh" >"$TEST_DIR/install.out" 2>"$TEST_DIR/install.err"; then
  fail 'installer accepted a sandbox path that resolves outside the sandbox'
fi
[[ ! -e "$ESCAPE_HOME/.claude-kimi" ]] || fail 'sandbox symlink escape changed the target configuration'
[[ ! -e "$ESCAPE_HOME/.local/bin/claude-kimi" ]] || fail 'sandbox symlink escape changed the target launcher'

mkdir -p "$ESCAPE_HOME/.claude-kimi/bin" "$ESCAPE_HOME/.local/bin"
printf '%s\n' 'claude-kimi-setup-version=1' > "$ESCAPE_HOME/.claude-kimi/.claude-kimi-setup-owned"
printf '%s\n' '# claude-kimi-setup-version=1' > "$ESCAPE_HOME/.local/bin/claude-kimi"
if CLAUDE_KIMI_INSTALL_ROOT="$SYMLINK_ROOT" \
  CLAUDE_KIMI_SKIP_KEYCHAIN=1 \
  CLAUDE_KIMI_ASSUME_YES=1 \
  "$ROOT_DIR/uninstall.sh" >"$TEST_DIR/uninstall.out" 2>"$TEST_DIR/uninstall.err"; then
  fail 'uninstaller accepted a sandbox path that resolves outside the sandbox'
fi
[[ -f "$ESCAPE_HOME/.local/bin/claude-kimi" ]] || fail 'sandbox symlink escape removed the target launcher'
rm -f "$SYMLINK_ROOT"
pass 'test controls reject sandbox symlink escapes'

mkdir -p "$NESTED_ROOT"
ln -s "$CHILD_ESCAPE_HOME" "$NESTED_ROOT/.local"
if CLAUDE_KIMI_INSTALL_ROOT="$NESTED_ROOT" \
  CLAUDE_KIMI_SKIP_KEYCHAIN=1 \
  "$ROOT_DIR/install.sh" >"$TEST_DIR/install.out" 2>"$TEST_DIR/install.err"; then
  fail 'installer accepted a nested destination symlink escape'
fi
[[ ! -e "$CHILD_ESCAPE_HOME/bin/claude-kimi" ]] || fail 'nested installer escape changed an external launcher'
rm -f "$NESTED_ROOT/.local"

mkdir -p "$NESTED_ROOT/.local/bin" "$CHILD_ESCAPE_HOME/bin"
printf '%s\n' 'claude-kimi-setup-version=1' > "$CHILD_ESCAPE_HOME/.claude-kimi-setup-owned"
printf '%s\n' 'fixture-settings' > "$CHILD_ESCAPE_HOME/settings.json"
printf '%s\n' 'fixture-helper' > "$CHILD_ESCAPE_HOME/bin/fireworks-key-helper"
ln -s "$CHILD_ESCAPE_HOME" "$NESTED_ROOT/.claude-kimi"
printf '%s\n' '# claude-kimi-setup-version=1' > "$NESTED_ROOT/.local/bin/claude-kimi"
if CLAUDE_KIMI_INSTALL_ROOT="$NESTED_ROOT" \
  CLAUDE_KIMI_SKIP_KEYCHAIN=1 \
  CLAUDE_KIMI_ASSUME_YES=1 \
  "$ROOT_DIR/uninstall.sh" >"$TEST_DIR/uninstall.out" 2>"$TEST_DIR/uninstall.err"; then
  fail 'uninstaller accepted a nested destination symlink escape'
fi
[[ -f "$CHILD_ESCAPE_HOME/.claude-kimi-setup-owned" ]] || fail 'nested uninstaller escape removed an external marker'
rm -f "$NESTED_ROOT/.claude-kimi"
pass 'managed destinations reject nested symlink escapes'

assert_mode() {
  local expected="$1"
  local path="$2"
  local actual
  actual="$(stat -f '%Lp' "$path")"
  [[ "$actual" == "$expected" ]] || fail "$path mode was $actual, expected $expected"
}

readonly INSTALL_HOME="$TEST_DIR/install-home"
mkdir -p "$INSTALL_HOME/.local/bin"
printf '%s\n' 'existing-kimi-command' > "$INSTALL_HOME/.local/bin/kimi"
kimi_hash_before="$(shasum -a 256 "$INSTALL_HOME/.local/bin/kimi" | awk '{print $1}')"

CLAUDE_KIMI_INSTALL_ROOT="$INSTALL_HOME" \
CLAUDE_KIMI_SKIP_KEYCHAIN=1 \
  "$ROOT_DIR/install.sh" >"$TEST_DIR/install.out" 2>"$TEST_DIR/install.err"

[[ -f "$INSTALL_HOME/.claude-kimi/settings.json" ]] || fail 'installer omitted settings.json'
[[ -x "$INSTALL_HOME/.claude-kimi/bin/fireworks-key-helper" ]] || fail 'installer omitted the key helper'
[[ -x "$INSTALL_HOME/.local/bin/claude-kimi" ]] || fail 'installer omitted the launcher'
[[ "$(sed -n '1p' "$INSTALL_HOME/.claude-kimi/.claude-kimi-setup-owned")" == 'claude-kimi-setup-version=1' ]] || fail 'installer omitted the ownership marker'
assert_mode 700 "$INSTALL_HOME/.claude-kimi"
assert_mode 600 "$INSTALL_HOME/.claude-kimi/settings.json"
assert_mode 700 "$INSTALL_HOME/.claude-kimi/bin/fireworks-key-helper"
assert_mode 700 "$INSTALL_HOME/.local/bin/claude-kimi"
kimi_hash_after="$(shasum -a 256 "$INSTALL_HOME/.local/bin/kimi" | awk '{print $1}')"
[[ "$kimi_hash_after" == "$kimi_hash_before" ]] || fail 'installer changed the existing kimi command'
pass 'installer creates isolated files with restrictive permissions'

if CLAUDE_KIMI_INSTALL_ROOT="$INSTALL_HOME" \
  CLAUDE_KIMI_SKIP_KEYCHAIN=1 \
  CLAUDE_KIMI_BACKUP_TIMESTAMP='../../../traversal-backup' \
  "$ROOT_DIR/install.sh" >"$TEST_DIR/install.out" 2>"$TEST_DIR/install.err"; then
  fail 'installer accepted a traversal backup timestamp'
fi
[[ ! -e "$TEST_DIR/traversal-backup" ]] || fail 'backup timestamp traversal wrote outside the installation root'
pass 'backup timestamp rejects path traversal'

CLAUDE_KIMI_INSTALL_ROOT="$INSTALL_HOME" \
CLAUDE_KIMI_SKIP_KEYCHAIN=1 \
CLAUDE_KIMI_BACKUP_TIMESTAMP=test-backup \
  "$ROOT_DIR/install.sh" >"$TEST_DIR/install.out" 2>"$TEST_DIR/install.err"

[[ -f "$INSTALL_HOME/.claude-kimi/backups/test-backup/settings.json" ]] || fail 'reinstall omitted settings backup'
[[ -f "$INSTALL_HOME/.claude-kimi/backups/test-backup/fireworks-key-helper" ]] || fail 'reinstall omitted helper backup'
[[ -f "$INSTALL_HOME/.claude-kimi/backups/test-backup/claude-kimi" ]] || fail 'reinstall omitted launcher backup'
[[ -f "$INSTALL_HOME/.claude-kimi/backups/test-backup/ownership-marker" ]] || fail 'reinstall omitted marker backup'
pass 'reinstall backs up setup-owned files'

settings_hash_before="$(shasum -a 256 "$INSTALL_HOME/.claude-kimi/settings.json" | awk '{print $1}')"
helper_hash_before="$(shasum -a 256 "$INSTALL_HOME/.claude-kimi/bin/fireworks-key-helper" | awk '{print $1}')"
launcher_hash_before="$(shasum -a 256 "$INSTALL_HOME/.local/bin/claude-kimi" | awk '{print $1}')"
: > "$TEST_DIR/security.calls"
if CLAUDE_KIMI_INSTALL_ROOT="$INSTALL_HOME" \
  CLAUDE_KIMI_TEST_SECURITY_BIN="$TEST_DIR/fake-security" \
  CLAUDE_KIMI_BACKUP_TIMESTAMP=rollback-backup \
  CLAUDE_KIMI_TEST_FAIL_AFTER_SETTINGS=1 \
  FAKE_SECURITY_CALLS="$TEST_DIR/security.calls" \
  "$ROOT_DIR/install.sh" >"$TEST_DIR/install.out" 2>"$TEST_DIR/install.err"; then
  fail 'failure-injection reinstall unexpectedly succeeded'
fi
[[ "$(shasum -a 256 "$INSTALL_HOME/.claude-kimi/settings.json" | awk '{print $1}')" == "$settings_hash_before" ]] || fail 'failed reinstall did not restore settings'
[[ "$(shasum -a 256 "$INSTALL_HOME/.claude-kimi/bin/fireworks-key-helper" | awk '{print $1}')" == "$helper_hash_before" ]] || fail 'failed reinstall did not restore the helper'
[[ "$(shasum -a 256 "$INSTALL_HOME/.local/bin/claude-kimi" | awk '{print $1}')" == "$launcher_hash_before" ]] || fail 'failed reinstall did not restore the launcher'
[[ ! -s "$TEST_DIR/security.calls" ]] || fail 'failed reinstall reached Keychain before active files completed'
pass 'failed reinstall restores every active file before Keychain access'

readonly COLLISION_HOME="$TEST_DIR/collision-home"
mkdir -p "$COLLISION_HOME/.local/bin"
printf '%s\n' 'unrelated-launcher' > "$COLLISION_HOME/.local/bin/claude-kimi"
collision_hash_before="$(shasum -a 256 "$COLLISION_HOME/.local/bin/claude-kimi" | awk '{print $1}')"
if CLAUDE_KIMI_INSTALL_ROOT="$COLLISION_HOME" \
  CLAUDE_KIMI_SKIP_KEYCHAIN=1 \
  "$ROOT_DIR/install.sh" >"$TEST_DIR/install.out" 2>"$TEST_DIR/install.err"; then
  fail 'installer overwrote an unrelated launcher'
fi
collision_hash_after="$(shasum -a 256 "$COLLISION_HOME/.local/bin/claude-kimi" | awk '{print $1}')"
[[ "$collision_hash_after" == "$collision_hash_before" ]] || fail 'collision refusal changed the unrelated launcher'
pass 'installer refuses unrelated targets without overwrite'

mkdir -p "$ADDKEY_HOME"
: > "$TEST_DIR/security.calls"
FAKE_SECURITY_MODE=stateful \
FAKE_SECURITY_CALLS="$TEST_DIR/security.calls" \
FAKE_SECURITY_STATE="$TEST_DIR/security.state" \
CLAUDE_KIMI_TEST_SECURITY_BIN="$TEST_DIR/fake-security" \
CLAUDE_KIMI_INSTALL_ROOT="$ADDKEY_HOME" \
  "$ROOT_DIR/install.sh" >"$TEST_DIR/install.out" 2>"$TEST_DIR/install.err"
grep -F 'add-generic-password' "$TEST_DIR/security.calls" >/dev/null || fail 'installer did not add a missing Keychain item'
if grep -F -- '-U' "$TEST_DIR/security.calls" >/dev/null; then
  fail 'installer used Keychain replacement mode for a missing item'
fi
if grep -F 'fw_fixture' "$TEST_DIR/security.calls" >/dev/null; then
  fail 'installer placed a key value in security command arguments'
fi
CLAUDE_KIMI_INSTALL_ROOT="$ADDKEY_HOME" \
CLAUDE_KIMI_SKIP_KEYCHAIN=1 \
CLAUDE_KIMI_ASSUME_YES=1 \
  "$ROOT_DIR/uninstall.sh" >"$TEST_DIR/uninstall.out" 2>"$TEST_DIR/uninstall.err"
pass 'installer adds a missing key without replacement or credential arguments'

mkdir -p "$KEYFAIL_HOME"
: > "$TEST_DIR/security.calls"
FAKE_SECURITY_MODE=valid \
FAKE_SECURITY_CALLS="$TEST_DIR/security.calls" \
CLAUDE_KIMI_TEST_SECURITY_BIN="$TEST_DIR/fake-security" \
CLAUDE_KIMI_INSTALL_ROOT="$KEYFAIL_HOME" \
  "$ROOT_DIR/install.sh" >"$TEST_DIR/install.out" 2>"$TEST_DIR/install.err"
if grep -F 'add-generic-password' "$TEST_DIR/security.calls" >/dev/null; then
  fail 'installer replaced an existing valid Keychain item'
fi
if FAKE_SECURITY_MODE=delete_error \
  FAKE_SECURITY_CALLS="$TEST_DIR/security.calls" \
  CLAUDE_KIMI_SECURITY_BIN="$TEST_DIR/fake-security" \
  CLAUDE_KIMI_TEST_SECURITY_BIN="$TEST_DIR/fake-security" \
  CLAUDE_KIMI_INSTALL_ROOT="$KEYFAIL_HOME" \
  CLAUDE_KIMI_ASSUME_YES=1 \
  "$ROOT_DIR/uninstall.sh" >"$TEST_DIR/uninstall.out" 2>"$TEST_DIR/uninstall.err"; then
  fail 'uninstaller reported success after a Keychain deletion error'
fi
if grep -F 'not present' "$TEST_DIR/uninstall.out" "$TEST_DIR/uninstall.err" >/dev/null; then
  fail 'uninstaller mislabeled a Keychain deletion error as absence'
fi
grep -F 'could not be deleted' "$TEST_DIR/uninstall.err" >/dev/null || fail 'uninstaller omitted the Keychain deletion error'
pass 'uninstaller reports Keychain deletion failures truthfully'

CLAUDE_KIMI_INSTALL_ROOT="$INSTALL_HOME" \
CLAUDE_KIMI_SKIP_KEYCHAIN=1 \
CLAUDE_KIMI_ASSUME_YES=1 \
  "$ROOT_DIR/uninstall.sh" >"$TEST_DIR/uninstall.out" 2>"$TEST_DIR/uninstall.err"

[[ ! -e "$INSTALL_HOME/.local/bin/claude-kimi" ]] || fail 'uninstaller left the launcher'
[[ ! -e "$INSTALL_HOME/.claude-kimi/settings.json" ]] || fail 'uninstaller left settings.json'
[[ ! -e "$INSTALL_HOME/.claude-kimi/bin/fireworks-key-helper" ]] || fail 'uninstaller left the helper'
[[ ! -e "$INSTALL_HOME/.claude-kimi/.claude-kimi-setup-owned" ]] || fail 'uninstaller left the ownership marker'
[[ -d "$INSTALL_HOME/.claude-kimi/backups/test-backup" ]] || fail 'uninstaller removed backups'
kimi_hash_after="$(shasum -a 256 "$INSTALL_HOME/.local/bin/kimi" | awk '{print $1}')"
[[ "$kimi_hash_after" == "$kimi_hash_before" ]] || fail 'uninstaller changed the existing kimi command'
pass 'uninstaller removes only active setup-owned files'

[[ -f "$ROOT_DIR/README.md" ]] || fail 'README.md is missing'
for documentation_anchor in \
  'bash /Users/xbtsupernode/Work/claude-kimi-setup/install.sh' \
  "claude-kimi -p 'Reply with exactly KIMI_OK' --output-format text --max-budget-usd 0.02" \
  'bash /Users/xbtsupernode/Work/claude-kimi-setup/uninstall.sh' \
  'accounts/fireworks/routers/kimi-k3-fast' \
  'https://api.fireworks.ai/inference'; do
  grep -F "$documentation_anchor" "$ROOT_DIR/README.md" >/dev/null || fail 'README.md omitted a required operations anchor'
done
pass 'README documents install, verification, provider, and rollback commands'

if grep -R -E 'fw_[A-Za-z0-9]{20,}' "$ROOT_DIR" >/dev/null; then
  fail 'package contains a value shaped like a Fireworks credential'
fi
forbidden_dash="$(printf '\342\200\224')"
if grep -R -F "$forbidden_dash" "$ROOT_DIR" >/dev/null; then
  fail 'package contains a forbidden Unicode dash'
fi
pass 'package scans contain no credential-shaped value or forbidden Unicode dash'
