from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

import yaml


@dataclass(frozen=True)
class SignalDecision:
    signal_id: str
    score: int
    action: str
    reason: str
    brief_path: Path | None


_DOMAINS = {"btc", "energy", "africa", "ai_infra", "manual"}
_PILLARS = {
    "builder_credibility",
    "nigeria_market_reality",
    "founder_lessons",
    "field_storytelling",
    "future_facing_authority",
}
_REQUIRED_FILES = (
    "nrg-bloom/marketing/intelligence/router-settings.yaml",
    "nrg-bloom/marketing/intelligence/signal-log.jsonl",
)


def ensure_intelligence_workspace(root: Path) -> None:
    intelligence_dir = root / "nrg-bloom" / "marketing" / "intelligence"
    intelligence_dir.mkdir(parents=True, exist_ok=True)
    settings_path = intelligence_dir / "router-settings.yaml"
    if not settings_path.exists():
        _write_yaml(
            settings_path,
            {
                "thresholds": {"auto_fire": 75, "advisory": 50},
                "weights": {
                    "business_proximity": 35,
                    "content_opportunity": 30,
                    "recency_window": 20,
                    "topic_pillar_fit": 15,
                },
                "cooldown_hours": 6,
                "pilot_mode": True,
            },
        )
    log_path = intelligence_dir / "signal-log.jsonl"
    if not log_path.exists():
        log_path.write_text("", encoding="utf-8")


def validate_intelligence_system(root: Path) -> list[str]:
    errors: list[str] = []
    for relative_path in _REQUIRED_FILES:
        if not (root / relative_path).exists():
            errors.append(f"missing required intelligence file: {relative_path}")
    return errors


def ingest_signal(
    root: Path,
    *,
    domain: str,
    headline: str,
    summary: str,
    nrg_angle: str,
    source: str,
    published_at: str,
    pillar: str,
    business_proximity: int,
    content_opportunity: int,
    recency_window: int,
    topic_pillar_fit: int,
) -> dict[str, Any]:
    ensure_intelligence_workspace(root)
    if domain not in _DOMAINS:
        raise ValueError(f"invalid domain: {domain}")
    if pillar not in _PILLARS:
        raise ValueError(f"invalid pillar: {pillar}")
    _validate_axis_score("business_proximity", business_proximity)
    _validate_axis_score("content_opportunity", content_opportunity)
    _validate_axis_score("recency_window", recency_window)
    _validate_axis_score("topic_pillar_fit", topic_pillar_fit)
    _parse_date(published_at)

    signal = {
        "id": _next_signal_id(root),
        "created_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "domain": domain,
        "headline": headline,
        "summary": summary,
        "nrg_angle": nrg_angle,
        "source": source,
        "published_at": published_at,
        "pillar": pillar,
        "scores": {
            "business_proximity": business_proximity,
            "content_opportunity": content_opportunity,
            "recency_window": recency_window,
            "topic_pillar_fit": topic_pillar_fit,
        },
        "router_decision": None,
    }
    _append_jsonl(root / "nrg-bloom" / "marketing" / "intelligence" / "signal-log.jsonl", signal)
    return signal


def route_signal(root: Path, *, signal_id: str, create_brief: bool, today: date | None = None) -> SignalDecision:
    ensure_intelligence_workspace(root)
    today = today or date.today()
    settings = _load_yaml(root / "nrg-bloom" / "marketing" / "intelligence" / "router-settings.yaml")
    thresholds = settings.get("thresholds", {})
    auto_fire_threshold = int(thresholds.get("auto_fire", 75))
    advisory_threshold = int(thresholds.get("advisory", 50))
    pilot_mode = bool(settings.get("pilot_mode", True))

    signals = _load_signals(root)
    signal = _find_signal(signals, signal_id)
    score = _weighted_score(signal["scores"], settings.get("weights", {}))
    if score >= auto_fire_threshold:
        action = "AUTO_FIRE"
        reason = "Signal crossed auto-fire threshold."
    elif score >= advisory_threshold:
        action = "ADVISORY"
        reason = "Signal is relevant but should be reviewed before generating content."
    else:
        action = "LOG_ONLY"
        reason = "Signal did not cross the relevance threshold."

    if pilot_mode and action == "AUTO_FIRE":
        action = "ADVISORY"
        reason = "Pilot mode is enabled, so auto-fire is downgraded to advisory."

    brief_path = None
    if create_brief and action in {"AUTO_FIRE", "ADVISORY"}:
        from .content import create_content_brief

        title = signal["headline"]
        idea = f"{signal['summary']} NRG Bloom angle: {signal['nrg_angle']}"
        brief = create_content_brief(root, title=title, idea=idea, suggested_date=None, today=today)
        brief_path = brief.brief_path

    signal["router_decision"] = {
        "score": score,
        "action": action,
        "reason": reason,
        "routed_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "brief_path": str(brief_path.relative_to(root)) if brief_path is not None else "",
    }
    _rewrite_signal_log(root, signals)
    return SignalDecision(signal_id=signal_id, score=score, action=action, reason=reason, brief_path=brief_path)


def signal_log_lines(root: Path) -> list[str]:
    ensure_intelligence_workspace(root)
    signals = _load_signals(root)
    lines = ["BloomFlow signal log"]
    if not signals:
        return lines + ["  none"]
    for signal in signals[-10:]:
        decision = signal.get("router_decision") or {}
        lines.append(
            f"  {signal.get('id', '')} [{signal.get('domain', '')}] {signal.get('headline', '')} "
            f"(score {decision.get('score', 'pending')}, action {decision.get('action', 'pending')})"
        )
    return lines


def intelligence_backend_payload(root: Path) -> dict[str, Any]:
    ensure_intelligence_workspace(root)
    signals = _load_signals(root)
    items = []
    for signal in signals:
        decision = signal.get("router_decision") or {}
        items.append(
            {
                "id": signal.get("id", ""),
                "domain": signal.get("domain", ""),
                "headline": signal.get("headline", ""),
                "pillar": signal.get("pillar", ""),
                "published_at": signal.get("published_at", ""),
                "score": decision.get("score"),
                "action": decision.get("action"),
                "brief_path": decision.get("brief_path", ""),
            }
        )
    return {
        "agent_name": "BloomFlow",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "signals": items,
    }


def write_intelligence_backend_payload(root: Path) -> Path:
    payload = intelligence_backend_payload(root)
    path = root / "nrg-bloom" / "marketing" / "generated" / "intelligence-summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
        temp_path = Path(handle.name)
    temp_path.replace(path)
    return path


def _weighted_score(scores: dict[str, Any], weights: dict[str, Any]) -> int:
    total = 0.0
    for key in ("business_proximity", "content_opportunity", "recency_window", "topic_pillar_fit"):
        weight = float(weights.get(key, 0))
        value = float(scores.get(key, 0))
        total += (value / 10.0) * weight
    return round(total)


def _next_signal_id(root: Path) -> str:
    highest = 0
    for signal in _load_signals(root):
        raw = str(signal.get("id", ""))
        if raw.startswith("SIG-"):
            try:
                highest = max(highest, int(raw.split("-", 1)[1]))
            except ValueError:
                continue
    return f"SIG-{highest + 1:03d}"


def _load_signals(root: Path) -> list[dict[str, Any]]:
    path = root / "nrg-bloom" / "marketing" / "intelligence" / "signal-log.jsonl"
    if not path.exists():
        return []
    signals: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            signals.append(json.loads(line))
    return signals


def _find_signal(signals: list[dict[str, Any]], signal_id: str) -> dict[str, Any]:
    for signal in signals:
        if str(signal.get("id", "")) == signal_id:
            return signal
    raise ValueError(f"signal not found: {signal_id}")


def _rewrite_signal_log(root: Path, signals: list[dict[str, Any]]) -> None:
    path = root / "nrg-bloom" / "marketing" / "intelligence" / "signal-log.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as handle:
        for signal in signals:
            handle.write(json.dumps(signal, ensure_ascii=True) + "\n")
        temp_path = Path(handle.name)
    temp_path.replace(path)


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not load as a mapping")
    return data


def _write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=False)
        temp_path = Path(handle.name)
    temp_path.replace(path)


def _validate_axis_score(name: str, value: int) -> None:
    if value < 0 or value > 10:
        raise ValueError(f"{name} must be between 0 and 10")


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()
