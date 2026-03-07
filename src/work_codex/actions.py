from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .filing import load_filing_package
from .litigation import litigation_deadlines, load_litigation_matter
from .workspace import Task, Workspace


@dataclass(frozen=True)
class StrategicAction:
    priority: str
    title: str
    rationale: str
    settlement_pressure: str


def build_strategic_actions(root: Path, today: date) -> list[StrategicAction]:
    matter = load_litigation_matter(root)
    package = load_filing_package(root)
    workspace = Workspace(root)
    tasks = workspace.tasks()
    overdue_deadlines, _ = litigation_deadlines(matter, today)
    actions: list[StrategicAction] = []

    if matter.protective_filing_needed != "no":
        actions.append(
            StrategicAction(
                priority="critical",
                title="Decide and prepare the protective Alberta filing path",
                rationale=(
                    "The Canadian track is still unresolved and the Axxela circumvention claim remains the main "
                    "cross-border leverage point."
                ),
                settlement_pressure=(
                    "A credible Alberta filing path makes it more expensive for TON to resist by preserving a second "
                    "front tied to the Axxela opportunity."
                ),
            )
        )

    if overdue_deadlines:
        actions.append(
            StrategicAction(
                priority="critical",
                title="Refresh the dispute clock and document the live negotiation posture",
                rationale="At least one tracked litigation deadline is already past in the live matter state.",
                settlement_pressure=(
                    "A clean live record reduces TON's ability to hide behind delay, drift, or ambiguity in the dispute process."
                ),
            )
        )

    if any(claim.claim_id == "C3" and claim.status == "needs_forum_review" for claim in package.claims):
        actions.append(
            StrategicAction(
                priority="high",
                title="Resolve forum treatment for the Axxela misrepresentation count",
                rationale="Claim C3 is factually mapped but still blocked on forum positioning.",
                settlement_pressure=(
                    "Locking the forum theory strengthens the July 4 Axxela pressure point and removes a drafting weakness."
                ),
            )
        )

    if any(claim.claim_id == "C4" and claim.status != "ready_to_plead" for claim in package.claims):
        actions.append(
            StrategicAction(
                priority="high",
                title="Quantify the unjust-enrichment and operations damages schedule",
                rationale="The services and expenditure theory is identified, but the damages schedule is still not tight enough.",
                settlement_pressure=(
                    "A cleaner quantified schedule makes low settlement numbers harder for TON to justify."
                ),
            )
        )

    if _find_task(tasks, "julie") or _find_task(tasks, "calculated tactic"):
        actions.append(
            StrategicAction(
                priority="high",
                title="Secure Julie's witness statement on the calculated-tactic admission",
                rationale="The witness statement remains one of the fastest ways to harden a contested oral admission.",
                settlement_pressure=(
                    "Turning the admission into a clearer witness artifact increases mediation and trial risk for TON."
                ),
            )
        )

    if _find_task(tasks, "2022 complaint") or _find_task(tasks, "phoenix trading"):
        actions.append(
            StrategicAction(
                priority="medium",
                title="Obtain the full 2022 complaint and outcome package",
                rationale="The prior lawsuit pattern is useful leverage but the record is still incomplete in the live queue.",
                settlement_pressure=(
                    "A fuller prior-pattern package increases reputational and litigation-cost pressure if TON forces escalation."
                ),
            )
        )

    if not actions:
        actions.append(
            StrategicAction(
                priority="medium",
                title="Refresh the draft bundle and maintain negotiation pressure",
                rationale="No immediate filing blocker was detected in the current matter state.",
                settlement_pressure="Regular refreshed work product signals readiness and keeps settlement pressure active.",
            )
        )
    return actions


def strategic_action_lines(root: Path, today: date) -> list[str]:
    matter = load_litigation_matter(root)
    actions = build_strategic_actions(root, today)
    lines = [
        f"strategic actions for {matter.matter}",
        "goal: make resistance more expensive than settlement while preserving filing readiness",
    ]
    for action in actions:
        lines.append(f"  [{action.priority}] {action.title}")
        lines.append(f"    why now: {action.rationale}")
        lines.append(f"    settlement pressure: {action.settlement_pressure}")
    return lines


def _find_task(tasks: list[Task], needle: str) -> Task | None:
    needle_lc = needle.lower()
    for task in tasks:
        haystack = f"{task.title}\n{task.notes}".lower()
        if needle_lc in haystack:
            return task
    return None
