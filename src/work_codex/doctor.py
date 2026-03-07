from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import platform
import sys


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str


def run_doctor(root: Path) -> list[CheckResult]:
    checks: list[CheckResult] = []
    checks.append(CheckResult("python", True, sys.version.split()[0]))
    checks.append(CheckResult("platform", True, f"{platform.system()} {platform.machine()}"))
    checks.append(_check_path(root / "src" / "work_codex", "runtime"))
    checks.append(_check_path(root / "shared", "shared workspace"))
    checks.append(_check_path(root / "knowledge", "knowledge store"))
    checks.append(_check_path(root / "nrg-bloom", "nrg-bloom workspace"))
    checks.append(_check_path(root / "nrg-bloom" / "litigation-ton" / "matter-status.yaml", "litigation matter status"))
    checks.append(_check_path(root / ".vendor" / "ruamel" / "yaml" / "__init__.py", "vendored yaml runtime"))
    checks.append(_check_optional(root / ".claude", "legacy claude adapter"))
    checks.append(_check_optional(root / ".mcp.json", "local MCP config"))
    return checks


def summarize_doctor(root: Path) -> tuple[bool, list[str]]:
    checks = run_doctor(root)
    ok = all(item.ok for item in checks if item.name != "legacy claude adapter" and item.name != "local MCP config")
    lines = []
    for item in checks:
        status = "ok" if item.ok else "missing"
        lines.append(f"{status:7} {item.name}: {item.detail}")
    return ok, lines


def _check_path(path: Path, name: str) -> CheckResult:
    return CheckResult(name, path.exists(), str(path))


def _check_optional(path: Path, name: str) -> CheckResult:
    detail = f"{path} ({'present' if path.exists() else 'optional'})"
    return CheckResult(name, True, detail)
