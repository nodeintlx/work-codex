# TON Daily Operating Procedure

This runbook is for daily operation of the TON litigation tool in the Work Codex repo.

Primary goal:
- make it more expensive for TON to fight than to settle

Secondary goal:
- keep the matter filing-ready at all times so settlement pressure remains credible

Repo root:

```bash
cd /home/dowsmasternode/repos/work-codex
```

## Operating Model

The system works best when you treat it as:
- the source of truth for case posture
- the place where new evidence gets converted into structured state
- the engine that tells you the next highest-leverage move

The human role is:
- bring in reality
- choose strategy
- approve external moves

The system role is:
- preserve the case state
- validate the record
- surface the next action
- generate internal work product

## Daily Cadence

Run this at the start of each day:

```bash
PYTHONPATH=src python3 -m work_codex.cli litigation-status --workspace .
PYTHONPATH=src python3 -m work_codex.cli filing-status --workspace .
PYTHONPATH=src python3 -m work_codex.cli litigation-next-actions --workspace .
PYTHONPATH=src python3 -m work_codex.cli scheduler-run --workspace . --cycles 1
PYTHONPATH=src python3 -m work_codex.cli draft-write-bundle --workspace .
```

This sequence answers five questions:

1. What is the live legal posture?
2. Are we still filing-ready?
3. What is the next highest-leverage move?
4. What is overdue or drifting?
5. What internal work product should exist today?

## Morning Procedure

Every morning:

1. Run the daily cadence commands.
2. Read [`nrg-bloom/litigation-ton/generated/latest/next-actions.md`](/home/dowsmasternode/repos/work-codex/nrg-bloom/litigation-ton/generated/latest/next-actions.md).
3. Read [`nrg-bloom/litigation-ton/generated/latest/alberta-protective-skeleton.md`](/home/dowsmasternode/repos/work-codex/nrg-bloom/litigation-ton/generated/latest/alberta-protective-skeleton.md).
4. Decide the single most important action for the day.
5. Update the live posture if the strategy has changed.

Morning objective:
- leave the first 15 minutes knowing the exact state of the case and the one move that increases pressure the most

## New Evidence Intake

When a new email, message, call summary, draft, or legal note arrives:

1. Save the file into the correct litigation folder.
2. Decide what changed:
   - chronology
   - evidence map
   - settlement posture
   - filing readiness
   - next actions
3. Ask Codex to absorb the change into the structured case state.
4. Regenerate the draft bundle.
5. Re-run `litigation-next-actions`.

The rule:
- no meaningful case development should live only in chat memory or in your head

It should end up reflected in:
- [`matter-status.yaml`](/home/dowsmasternode/repos/work-codex/nrg-bloom/litigation-ton/matter-status.yaml)
- [`settlement-tracker.yaml`](/home/dowsmasternode/repos/work-codex/nrg-bloom/litigation-ton/settlement-tracker.yaml)
- [`claims-map.yaml`](/home/dowsmasternode/repos/work-codex/nrg-bloom/litigation-ton/claims-map.yaml)
- [`chronology-map.yaml`](/home/dowsmasternode/repos/work-codex/nrg-bloom/litigation-ton/chronology-map.yaml)
- [`evidence-map.yaml`](/home/dowsmasternode/repos/work-codex/nrg-bloom/litigation-ton/evidence-map.yaml)

## Pressure-Building Priorities

The system is currently optimized around these pressure levers:

1. Protective Alberta filing credibility
2. Clean and current dispute clock
3. Axxela misrepresentation and circumvention structure
4. Quantified unjust-enrichment and operations damages
5. Julie witness statement on the calculated-tactic admission
6. Phoenix Trading / prior-pattern package

Decision rule:
- if a task increases filing credibility or raises TON's litigation risk, it is usually higher value than a generic research task

## Before Any External Move

Before sending anything to TON, counsel, or a third party:

1. Run:

```bash
PYTHONPATH=src python3 -m work_codex.cli filing-validate --workspace .
PYTHONPATH=src python3 -m work_codex.cli litigation-next-actions --workspace .
PYTHONPATH=src python3 -m work_codex.cli draft-write-bundle --workspace .
```

2. Check that the bundle reflects the current posture.
3. Confirm whether the move:
   - increases settlement pressure
   - weakens filing leverage
   - reveals evidence too early
   - changes forum positioning

Do not make an external move from stale state.

## Negotiation / Settlement Use

When the objective is settlement pressure:

Use the system to answer:
- what is the strongest leverage point today?
- what evidence should remain held back?
- what missing artifact makes our pressure less credible?
- what would TON least want to see become filing-ready?

Good settlement-pressure outputs are:
- updated claim outline
- refreshed facts section
- Alberta protective filing skeleton
- next-actions memo
- quantified damages support

## End-of-Day Procedure

At the end of the day:

1. Update any posture or settlement changes.
2. Record any completed or newly blocked tasks.
3. Regenerate the draft bundle if the matter changed.
4. Check that tomorrow's most important action is explicit.

Recommended closeout commands:

```bash
PYTHONPATH=src python3 -m work_codex.cli litigation-next-actions --workspace .
PYTHONPATH=src python3 -m work_codex.cli draft-write-bundle --workspace .
```

End-of-day objective:
- if you stop working unexpectedly, the system should still tell the truth about where the case stands

## Weekly Review

Once per week:

1. Review all strategic actions.
2. Re-check the damages schedule quality.
3. Re-check the Alberta filing track.
4. Re-check whether held-back evidence should remain held back.
5. Re-check whether the settlement floor or current posture needs to change.

Weekly question:
- are we becoming more credible, more dangerous to fight, and more ready to file?

## High-Discipline Rules

- Do not let live posture drift from reality.
- Do not let key evidence remain unstructured after it becomes important.
- Do not negotiate from stale drafts.
- Do not let the Canadian path remain vague for too long.
- Do not confuse activity with leverage.

The best use of the system is not to generate more text.
The best use is to keep the case sharper, more current, and more expensive for TON to resist.
