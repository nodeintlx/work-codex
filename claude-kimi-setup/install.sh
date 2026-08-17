#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
readonly INSTALL_ROOT="${CLAUDE_KIMI_INSTALL_ROOT:-$HOME}"
readonly CONFIG_DIR="$INSTALL_ROOT/.claude-kimi"
readonly HELPER_DIR="$CONFIG_DIR/bin"
readonly LOCAL_DIR="$INSTALL_ROOT/.local"
readonly BIN_DIR="$LOCAL_DIR/bin"
readonly BACKUPS_DIR="$CONFIG_DIR/backups"
readonly LAUNCHER_FILE="$BIN_DIR/claude-kimi"
readonly SETTINGS_FILE="$CONFIG_DIR/settings.json"
readonly HELPER_FILE="$HELPER_DIR/fireworks-key-helper"
readonly MARKER_FILE="$CONFIG_DIR/.claude-kimi-setup-owned"
readonly MARKER_VALUE='claude-kimi-setup-version=1'
readonly KEYCHAIN_SERVICE='com.makir.claude-kimi.fireworks'
readonly SKIP_KEYCHAIN="${CLAUDE_KIMI_SKIP_KEYCHAIN:-0}"
readonly TEST_FAIL_AFTER_SETTINGS="${CLAUDE_KIMI_TEST_FAIL_AFTER_SETTINGS:-0}"

SECURITY_BIN='/usr/bin/security'
BACKUP_DIR=''
ORIGINAL_CONFIG_DIR=0
ORIGINAL_HELPER_DIR=0
ORIGINAL_BIN_DIR=0
ORIGINAL_SETTINGS=0
ORIGINAL_HELPER=0
ORIGINAL_LAUNCHER=0
ORIGINAL_MARKER=0
TRANSACTION_ACTIVE=0

fail() {
  printf 'claude-kimi installer: %s\n' "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "required command not found: $1"
}

is_test_sandbox() {
  local canonical_home
  local canonical_install_root

  [[ -n "${CLAUDE_KIMI_INSTALL_ROOT:-}" ]] || return 1
  [[ -d "$INSTALL_ROOT" && ! -L "$INSTALL_ROOT" ]] || return 1
  canonical_install_root="$(cd "$INSTALL_ROOT" && pwd -P)" || return 1
  canonical_home="$(cd "$HOME" && pwd -P)" || return 1
  [[ "$canonical_install_root" != "$canonical_home" ]] || return 1
  [[ "$canonical_install_root" == /private/tmp/claude-kimi-* ]]
}

select_security_bin() {
  local candidate
  local candidate_dir
  local canonical_candidate

  candidate="${CLAUDE_KIMI_TEST_SECURITY_BIN:-}"
  [[ -n "$candidate" ]] || return 0
  is_test_sandbox || fail 'the Keychain test seam is permitted only in the test sandbox'
  [[ -x "$candidate" && ! -L "$candidate" ]] || fail 'the Keychain test executable is invalid'
  candidate_dir="$(cd "$(dirname "$candidate")" && pwd -P)" || fail 'the Keychain test path is invalid'
  canonical_candidate="$candidate_dir/$(basename "$candidate")"
  [[ "$canonical_candidate" == /private/tmp/claude-kimi-* ]] ||
    fail 'the Keychain test executable resolves outside the test sandbox'
  SECURITY_BIN="$canonical_candidate"
}

validate_test_controls() {
  if [[ "$SKIP_KEYCHAIN" == '1' || "$TEST_FAIL_AFTER_SETTINGS" == '1' ||
    -n "${CLAUDE_KIMI_BACKUP_TIMESTAMP:-}" ||
    -n "${CLAUDE_KIMI_TEST_SECURITY_BIN:-}" ]]; then
    is_test_sandbox || fail 'test controls are permitted only in the test sandbox'
  fi
  [[ "$TEST_FAIL_AFTER_SETTINGS" == '0' || "$TEST_FAIL_AFTER_SETTINGS" == '1' ]] ||
    fail 'invalid failure-injection value'
}

validate_managed_paths() {
  local canonical_install_root
  local canonical_managed_directory
  local managed_directory
  local managed_file

  [[ -d "$INSTALL_ROOT" ]] || fail "installation root is not a directory: $INSTALL_ROOT"
  canonical_install_root="$(cd "$INSTALL_ROOT" && pwd -P)" ||
    fail "installation root cannot be resolved: $INSTALL_ROOT"

  for managed_directory in \
    "$LOCAL_DIR" \
    "$BIN_DIR" \
    "$CONFIG_DIR" \
    "$HELPER_DIR" \
    "$BACKUPS_DIR"; do
    [[ ! -L "$managed_directory" ]] || fail "refusing symlinked managed directory: $managed_directory"
    if [[ -e "$managed_directory" ]]; then
      [[ -d "$managed_directory" ]] || fail "managed directory path is not a directory: $managed_directory"
      canonical_managed_directory="$(cd "$managed_directory" && pwd -P)" ||
        fail "managed directory cannot be resolved: $managed_directory"
      case "$canonical_managed_directory" in
        "$canonical_install_root"|"$canonical_install_root"/*) ;;
        *) fail "managed directory resolves outside the installation root: $managed_directory" ;;
      esac
    fi
  done

  for managed_file in "$LAUNCHER_FILE" "$SETTINGS_FILE" "$HELPER_FILE" "$MARKER_FILE"; do
    [[ ! -L "$managed_file" ]] || fail "refusing symlinked managed file: $managed_file"
    [[ ! -e "$managed_file" || -f "$managed_file" ]] ||
      fail "managed file path is not a regular file: $managed_file"
  done
}

validate_sources() {
  local source_file
  for source_file in settings.json fireworks-key-helper claude-kimi; do
    [[ -f "$SCRIPT_DIR/$source_file" ]] || fail "source file is missing: $source_file"
  done

  bash -n "$SCRIPT_DIR/fireworks-key-helper"
  bash -n "$SCRIPT_DIR/claude-kimi"
  node -e 'JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"))' \
    "$SCRIPT_DIR/settings.json"
}

refuse_unowned_targets() {
  if [[ -e "$CONFIG_DIR" ]]; then
    [[ -f "$MARKER_FILE" ]] || fail "refusing unowned configuration directory: $CONFIG_DIR"
    [[ "$(sed -n '1p' "$MARKER_FILE")" == "$MARKER_VALUE" ]] ||
      fail "refusing configuration with an unknown ownership marker: $CONFIG_DIR"
  fi

  if [[ -e "$LAUNCHER_FILE" ]]; then
    [[ -f "$MARKER_FILE" ]] || fail "refusing unrelated launcher: $LAUNCHER_FILE"
    grep -F "$MARKER_VALUE" "$LAUNCHER_FILE" >/dev/null 2>&1 ||
      fail "refusing launcher without the setup ownership marker: $LAUNCHER_FILE"
  fi
}

store_and_validate_keychain_item() {
  local account
  local api_key
  local find_status
  local delete_status

  if [[ "$SKIP_KEYCHAIN" == '1' ]]; then
    printf 'Keychain: skipped in validated test sandbox\n'
    return
  fi

  [[ -x "$SECURITY_BIN" ]] || fail 'macOS Keychain security command is unavailable'
  account="$(id -un)"
  api_key=''
  if api_key="$(
    "$SECURITY_BIN" find-generic-password \
      -a "$account" \
      -s "$KEYCHAIN_SERVICE" \
      -w 2>/dev/null
  )"; then
    case "$api_key" in
      fw_?*) ;;
      *)
        unset api_key
        fail 'the existing Keychain item is not a standard Fireworks fw_ key'
        ;;
    esac
    unset api_key
    printf 'Keychain: preserved existing standard Fireworks key\n'
    printf 'Key type: fw_\n'
    return
  else
    find_status=$?
  fi
  unset api_key
  [[ "$find_status" == '44' ]] || fail 'the existing Keychain item could not be checked'

  printf 'Enter the new standard Fireworks fw_ key in the macOS Keychain prompt.\n'
  "$SECURITY_BIN" add-generic-password \
    -a "$account" \
    -s "$KEYCHAIN_SERVICE" \
    -w

  api_key=''
  if ! api_key="$(
    "$SECURITY_BIN" find-generic-password \
      -a "$account" \
      -s "$KEYCHAIN_SERVICE" \
      -w 2>/dev/null
  )"; then
    unset api_key
    if "$SECURITY_BIN" delete-generic-password \
      -a "$account" \
      -s "$KEYCHAIN_SERVICE" >/dev/null 2>&1; then
      fail 'the new Keychain item could not be validated and was removed'
    else
      delete_status=$?
    fi
    fail "the new Keychain item could not be validated or removed (security exit $delete_status)"
  fi
  case "$api_key" in
    fw_?*) ;;
    *)
      unset api_key
      if "$SECURITY_BIN" delete-generic-password \
        -a "$account" \
        -s "$KEYCHAIN_SERVICE" >/dev/null 2>&1; then
        fail 'the new Keychain item was not a standard Fireworks fw_ key and was removed'
      else
        delete_status=$?
      fi
      fail "the invalid new Keychain item could not be removed (security exit $delete_status)"
      ;;
  esac
  unset api_key
  printf 'Key type: fw_\n'
}

backup_owned_targets() {
  local canonical_backup_dir
  local canonical_backups_dir
  local timestamp

  [[ -f "$MARKER_FILE" ]] || return 0

  if [[ -n "${CLAUDE_KIMI_BACKUP_TIMESTAMP:-}" ]]; then
    is_test_sandbox || fail 'fixed backup timestamps are permitted only in the test sandbox'
    timestamp="$CLAUDE_KIMI_BACKUP_TIMESTAMP"
  else
    timestamp="$(date +%Y%m%d-%H%M%S)"
  fi
  case "$timestamp" in
    ''|'.'|'..'|*[!A-Za-z0-9._-]*) fail 'backup timestamp must be a safe single basename' ;;
  esac

  install -d -m 0700 "$BACKUPS_DIR"
  [[ ! -L "$BACKUPS_DIR" ]] || fail "refusing symlinked backups directory: $BACKUPS_DIR"
  canonical_backups_dir="$(cd "$BACKUPS_DIR" && pwd -P)" ||
    fail "backups directory cannot be resolved: $BACKUPS_DIR"
  BACKUP_DIR="$BACKUPS_DIR/$timestamp"
  [[ ! -e "$BACKUP_DIR" && ! -L "$BACKUP_DIR" ]] || fail "backup already exists: $BACKUP_DIR"
  install -d -m 0700 "$BACKUP_DIR"
  canonical_backup_dir="$(cd "$BACKUP_DIR" && pwd -P)" ||
    fail "backup directory cannot be resolved: $BACKUP_DIR"
  case "$canonical_backup_dir" in
    "$canonical_backups_dir"/*) ;;
    *) fail "backup directory resolves outside the managed backups directory: $BACKUP_DIR" ;;
  esac

  [[ ! -f "$SETTINGS_FILE" ]] || cp -p "$SETTINGS_FILE" "$BACKUP_DIR/settings.json"
  [[ ! -f "$HELPER_FILE" ]] || cp -p "$HELPER_FILE" "$BACKUP_DIR/fireworks-key-helper"
  [[ ! -f "$LAUNCHER_FILE" ]] || cp -p "$LAUNCHER_FILE" "$BACKUP_DIR/claude-kimi"
  cp -p "$MARKER_FILE" "$BACKUP_DIR/ownership-marker"
  printf 'Backup: %s\n' "$BACKUP_DIR"
}

record_active_state() {
  [[ ! -d "$CONFIG_DIR" ]] || ORIGINAL_CONFIG_DIR=1
  [[ ! -d "$HELPER_DIR" ]] || ORIGINAL_HELPER_DIR=1
  [[ ! -d "$BIN_DIR" ]] || ORIGINAL_BIN_DIR=1
  [[ ! -f "$SETTINGS_FILE" ]] || ORIGINAL_SETTINGS=1
  [[ ! -f "$HELPER_FILE" ]] || ORIGINAL_HELPER=1
  [[ ! -f "$LAUNCHER_FILE" ]] || ORIGINAL_LAUNCHER=1
  [[ ! -f "$MARKER_FILE" ]] || ORIGINAL_MARKER=1
}

restore_or_remove_file() {
  local existed_before="$1"
  local backup_file="$2"
  local active_file="$3"

  if [[ "$existed_before" == '1' && -f "$backup_file" ]]; then
    cp -p "$backup_file" "$active_file"
    printf 'Rollback restored: %s\n' "$active_file" >&2
  elif [[ "$existed_before" == '0' ]]; then
    rm -f "$active_file"
    printf 'Rollback removed: %s\n' "$active_file" >&2
  fi
}

rollback_installation() {
  local status="$?"
  [[ "$TRANSACTION_ACTIVE" == '1' && "$status" != '0' ]] || return "$status"

  set +e
  restore_or_remove_file "$ORIGINAL_SETTINGS" "$BACKUP_DIR/settings.json" "$SETTINGS_FILE"
  restore_or_remove_file "$ORIGINAL_HELPER" "$BACKUP_DIR/fireworks-key-helper" "$HELPER_FILE"
  restore_or_remove_file "$ORIGINAL_LAUNCHER" "$BACKUP_DIR/claude-kimi" "$LAUNCHER_FILE"
  restore_or_remove_file "$ORIGINAL_MARKER" "$BACKUP_DIR/ownership-marker" "$MARKER_FILE"
  [[ "$ORIGINAL_HELPER_DIR" == '1' ]] || rmdir "$HELPER_DIR" 2>/dev/null
  [[ "$ORIGINAL_CONFIG_DIR" == '1' ]] || rmdir "$CONFIG_DIR" 2>/dev/null
  [[ "$ORIGINAL_BIN_DIR" == '1' ]] || rmdir "$BIN_DIR" 2>/dev/null
  printf 'claude-kimi installer: active files were rolled back after failure\n' >&2
  return "$status"
}

install_files() {
  if [[ ! -d "$BIN_DIR" ]]; then
    install -d -m 0700 "$BIN_DIR"
  fi
  install -d -m 0700 "$CONFIG_DIR" "$HELPER_DIR"

  printf '%s\n' "$MARKER_VALUE" > "$MARKER_FILE"
  chmod 0600 "$MARKER_FILE"
  install -m 0600 "$SCRIPT_DIR/settings.json" "$SETTINGS_FILE"
  if [[ "$TEST_FAIL_AFTER_SETTINGS" == '1' ]]; then
    return 97
  fi
  install -m 0700 "$SCRIPT_DIR/fireworks-key-helper" "$HELPER_FILE"
  install -m 0700 "$SCRIPT_DIR/claude-kimi" "$LAUNCHER_FILE"
}

print_summary() {
  printf 'Installed configuration: %s\n' "$CONFIG_DIR"
  printf 'Installed launcher: %s\n' "$LAUNCHER_FILE"
  printf 'Model router: accounts/fireworks/routers/kimi-k3-fast\n'
  printf 'Existing claude and kimi commands were not modified.\n'
}

for required in bash chmod cp date grep id install node sed; do
  require_command "$required"
done
validate_sources
validate_test_controls
select_security_bin
validate_managed_paths
refuse_unowned_targets
record_active_state
backup_owned_targets
TRANSACTION_ACTIVE=1
trap rollback_installation EXIT
install_files
store_and_validate_keychain_item
TRANSACTION_ACTIVE=0
trap - EXIT
print_summary
