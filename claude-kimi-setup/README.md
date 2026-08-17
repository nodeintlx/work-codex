# Claude Code with Fireworks Kimi K3

This package installs a separate `claude-kimi` command that uses the existing Claude Code interface with Fireworks Kimi K3. It does not modify the normal `claude` command or the existing `kimi` command.

## Result

```text
claude       -> Claude Code -> existing first-party Anthropic setup
claude-kimi  -> Claude Code -> Fireworks -> Kimi K3 Fast
kimi         -> existing command, unchanged
```

The Kimi configuration lives under `~/.claude-kimi`. The Fireworks key lives in macOS Keychain under service `com.makir.claude-kimi.fireworks`.

## Before installation

1. Sign in to the [Fireworks dashboard](https://app.fireworks.ai/api-keys).
2. Create a new standard pay-per-use API key whose prefix is `fw_`.
3. Do not paste the key into chat, a repository, a shell command, or a Claude settings file.

Kimi requests made with this key are billed at Fireworks pay-per-use rates.

## Install

Run this from a local terminal:

```bash
bash /Users/xbtsupernode/Work/claude-kimi-setup/install.sh
```

If the setup has no Keychain item yet, the installer opens a macOS Keychain prompt. Enter the new `fw_` key only in that prompt. The key is not passed as a command argument and is not written into the Claude settings file. A valid existing item is preserved instead of overwritten.

The installer creates:

```text
~/.claude-kimi/settings.json
~/.claude-kimi/bin/fireworks-key-helper
~/.claude-kimi/.claude-kimi-setup-owned
~/.local/bin/claude-kimi
```

It does not install FireConnect, edit shell startup files, copy user-level Claude plugins, or modify `~/.claude`.

## Use

Start an interactive Kimi-backed Claude Code session:

```bash
claude-kimi
```

Normal Claude Code arguments are forwarded:

```bash
claude-kimi --continue
claude-kimi --resume
claude-kimi --help
```

Every default model slot uses:

```text
accounts/fireworks/routers/kimi-k3-fast
```

The provider base URL is:

```text
https://api.fireworks.ai/inference
```

Claude Code permission controls remain enabled. The setup does not enable any permission-bypass mode.

## Verify

Before installation, record the normal provider and settings hash:

```bash
claude auth status --json
shasum -a 256 ~/.claude/settings.json
command -v kimi
```

After installation, confirm argument forwarding:

```bash
claude-kimi --help
```

From a non-confidential directory, run one low-budget inference check:

```bash
claude-kimi -p 'Reply with exactly KIMI_OK' --output-format text --max-budget-usd 0.02
```

Expected output:

```text
KIMI_OK
```

Then confirm normal Claude remains first-party and the existing settings and `kimi` path remain unchanged:

```bash
claude auth status --json
shasum -a 256 ~/.claude/settings.json
command -v kimi
```

## Troubleshooting

- If the Keychain helper reports a missing key, rerun the installer and enter the standard `fw_` key in the Keychain prompt.
- To rotate the key later, delete the `com.makir.claude-kimi.fireworks` item in the macOS Keychain Access application, then rerun the installer. Do this only when rotation is intentional.
- If Fireworks rejects `accounts/fireworks/routers/kimi-k3-fast` for the standard key, stop and report the sanitized error. Do not substitute another model.
- Do not enable Claude Code debug logging while diagnosing authentication. Debug output may contain request headers.
- User-level plugins and customizations from `~/.claude` are intentionally not copied. Project-level Claude settings and instructions still load normally.
- FireConnect is intentionally absent because its standard Claude integration changes the normal user settings instead of providing the required isolation.

## Roll back

Run:

```bash
bash /Users/xbtsupernode/Work/claude-kimi-setup/uninstall.sh
```

The uninstaller validates the setup ownership marker before removing active files. It asks separately before permanently deleting the Keychain credential. Backups and Kimi session data are preserved, and the normal `claude` and existing `kimi` commands are untouched.

If a reinstall fails after changing an active setup file, the installer restores every prior active file automatically and reports each restored path. The timestamped backup remains under `~/.claude-kimi/backups` for inspection.

To restore a backup manually, first list and inspect the timestamped directories:

```bash
find ~/.claude-kimi/backups -mindepth 1 -maxdepth 1 -type d -print
```

After selecting the exact timestamp, restore only the setup-owned files:

```bash
claude_kimi_backup=~/.claude-kimi/backups/YYYYMMDD-HHMMSS
install -m 0600 "$claude_kimi_backup/settings.json" ~/.claude-kimi/settings.json
install -m 0700 "$claude_kimi_backup/fireworks-key-helper" ~/.claude-kimi/bin/fireworks-key-helper
install -m 0700 "$claude_kimi_backup/claude-kimi" ~/.local/bin/claude-kimi
install -m 0600 "$claude_kimi_backup/ownership-marker" ~/.claude-kimi/.claude-kimi-setup-owned
```

Replace the timestamp placeholder with a directory you inspected. These commands do not change the Keychain item.

## Test the package

The automated suite writes only to a temporary sandbox:

```bash
LC_ALL=C LANG=C bash /Users/xbtsupernode/Work/claude-kimi-setup/tests/test-claude-kimi-setup.sh
```

Official references:

- [Claude Code environment variables](https://code.claude.com/docs/en/env-vars)
- [Claude Code LLM gateway configuration](https://code.claude.com/docs/en/llm-gateway)
- [Fireworks Claude Code integration](https://docs.fireworks.ai/ecosystem/fireconnect/claude-code)
- [Fireworks Kimi K3 router](https://docs.fireworks.ai/firepass)
- [Fireworks Anthropic compatibility](https://docs.fireworks.ai/tools-sdks/anthropic-compatibility)
