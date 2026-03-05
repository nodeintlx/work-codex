---
name: pipeline
description: >-
  Business development pipeline status — all active deals, prospects, and
  partnership opportunities across NRG Bloom and Coldstorm AI.
user-invocable: true
---

Trigger the pipeline-tracker skill to review all active business development opportunities.

## Execution

1. **Load pipeline** — Read ~/Work/shared/pipeline.yaml. If it does not exist, build it from tasks.yaml and known deals.

2. **Check email** — Use `gws` CLI to search for responses from pipeline contacts:
   ```bash
   gws gmail users messages list --params '{"userId": "me", "q": "is:unread from:oandoenergy.com OR from:eleas OR from:chioma"}'
   ```
   Also check for new business inquiries.

3. **Cross-reference tasks** — Ensure pipeline next_actions and tasks.yaml are aligned.

4. **Flag stale deals** — Any deal with no contact in 7+ days gets flagged with recommended action.

5. **OKR check** — Cross-reference goals.yaml for partnership/client key results. Surface gaps.

6. **Present dashboard** — Follow the pipeline-tracker skill output format.

## Context
- NRG Bloom: focus on energy partnerships (Oando, future prospects)
- Coldstorm: client inquiries, consulting opportunities
- Suggest new prospects based on market research
