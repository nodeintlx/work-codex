#!/usr/bin/env bash
set -euo pipefail

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
readonly ASSUME_YES="${CLAUDE_KIMI_ASSUME_YES:-0}"
SECURITY_BIN='/usr/bin/security'

fail() {
  printf 'claude-kimi uninstaller: %s\n' "$*" >&2
  exit 1
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

confirm_removal() {
  local answer
  if [[ "$ASSUME_YES" == '1' ]]; then
    is_test_sandbox || fail 'automatic confirmation is permitted only in the test sandbox'
    return
  fi

  printf 'Remove the active claude-kimi launcher and isolated provider settings? [y/N] '
  read -r answer
  [[ "$answer" == 'y' || "$answer" == 'Y' ]] || fail 'cancelled'
}

confirm_keychain_removal() {
  local answer
  if [[ "$SKIP_KEYCHAIN" == '1' ]]; then
    is_test_sandbox || fail 'Keychain bypass is permitted only in the test sandbox'
    return 1
  fi
  if [[ "$ASSUME_YES" == '1' ]]; then
    is_test_sandbox || fail 'automatic Keychain confirmation is permitted only in the test sandbox'
    return 0
  fi

  printf 'Also permanently delete the Fireworks Keychain item? [y/N] '
  read -r answer
  [[ "$answer" == 'y' || "$answer" == 'Y' ]]
}

remove_active_file() {
  local target="$1"
  [[ -e "$target" ]] || return 0
  rm -f "$target"
  printf 'Removed: %s\n' "$target"
}

validate_managed_paths
[[ -f "$MARKER_FILE" ]] || fail "ownership marker not found: $MARKER_FILE"
[[ "$(sed -n '1p' "$MARKER_FILE")" == "$MARKER_VALUE" ]] ||
  fail "unknown ownership marker: $MARKER_FILE"
if [[ -e "$LAUNCHER_FILE" ]]; then
  grep -F "$MARKER_VALUE" "$LAUNCHER_FILE" >/dev/null 2>&1 ||
    fail "refusing unrelated launcher: $LAUNCHER_FILE"
fi
if [[ "$SKIP_KEYCHAIN" == '1' || "$ASSUME_YES" == '1' ]]; then
  is_test_sandbox || fail 'test controls are permitted only in the test sandbox'
fi
select_security_bin

confirm_removal
delete_keychain=0
if confirm_keychain_removal; then
  delete_keychain=1
fi

remove_active_file "$LAUNCHER_FILE"
remove_active_file "$SETTINGS_FILE"
remove_active_file "$HELPER_FILE"
remove_active_file "$MARKER_FILE"
rmdir "$HELPER_DIR" 2>/dev/null || true
rmdir "$CONFIG_DIR" 2>/dev/null || true

if [[ "$delete_keychain" == '1' ]]; then
  if "$SECURITY_BIN" delete-generic-password \
    -a "$(id -un)" \
    -s "$KEYCHAIN_SERVICE" >/dev/null 2>&1; then
    printf 'Deleted Keychain service: %s (not recoverable)\n' "$KEYCHAIN_SERVICE"
  else
    delete_status=$?
    if [[ "$delete_status" == '44' ]]; then
      if "$SECURITY_BIN" find-generic-password \
        -a "$(id -un)" \
        -s "$KEYCHAIN_SERVICE" >/dev/null 2>&1; then
        fail 'Keychain deletion reported absence, but the item is still present'
      else
        find_status=$?
      fi
      if [[ "$find_status" == '44' ]]; then
        printf 'Keychain service was not present: %s\n' "$KEYCHAIN_SERVICE"
      else
        fail "Keychain absence could not be verified (security exit $find_status)"
      fi
    else
      fail "Keychain service could not be deleted (security exit $delete_status)"
    fi
  fi
else
  printf 'Preserved Keychain service: %s\n' "$KEYCHAIN_SERVICE"
fi

printf 'Removed active claude-kimi files. Backups and session data were preserved.\n'
printf 'Existing claude and kimi commands were not modified.\n'
