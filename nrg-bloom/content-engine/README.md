# NRG Bloom Content Engine

Codex's content engine for NRG Bloom is built around one assumption:
authority will come from operator truth, not generic thought-leadership.

This system is designed to generate content that feels like it came from a
company actually building remote compute infrastructure in Africa.

## What Makes This Different

- Brand-locked: uses the same core palette and type direction as the NRG Bloom website rebuild
- Operator-led: prioritizes remote deployment, gas monetization, and field execution over abstract industry commentary
- Multi-format: every brief can generate LinkedIn, X, carousel, video script, motion scene spec, branded cards, and portrait quote cards for X/LinkedIn
- Campaign-based: content is organized into weekly or thematic authority sprints instead of one-off posts
- Source-aware: verified claims can now be `internal`, `external`, or `hybrid`, with provenance attached to each source

## Editorial Franchises

- `builder-ledger`: hard numbers and field economics
- `remote-ops-notebook`: lessons from running infrastructure remotely from Montreal into African sites
- `energy-to-compute-thesis`: why stranded energy becomes sovereign compute capacity
- `africa-infrastructure-myths`: sharp rebuttals to lazy frontier-market assumptions

## Brand Rules

- Deep navy base with teal accent and amber support
- Space Grotesk for display, Inter for body
- Serious industrial tone, not crypto-casino aesthetics
- No hype words unless directly earned by proof

## Usage

From the repo root:

```bash
PYTHONPATH=src python3 -m work_codex.cli content-campaign-generate --workspace . --campaign nrg-bloom/content-engine/campaigns/2026-03-26-authority-sprint.yaml
```

Generated output lands in:

```text
nrg-bloom/content-engine/generated/<timestamp>-<campaign-slug>/
```

Each brief gets:

- `linkedin-founder.md`
- `linkedin-company.md`
- `x-thread.md`
- `carousel.md`
- `video-script.md`
- `tiktok-caption.md`
- `video-scenes.json`
- `social-card.html`
- `quote-card-portrait.html`
- `quote-card-portrait.png`

Each campaign root also gets:

- `quote-cards.html`

Verified campaigns also get:

- `factcheck-report.md`
- `<brief>/verification.md`
- `<brief>/verification.json`
- rendered proof assets in `motion-pack/`

## Verification Model

- `internal`: NRG Bloom records and operating documentation
- `external`: public datasets, regulators, multilaterals, and trusted media
- `hybrid`: NRG Bloom experience combined with external market evidence

The engine expects at least 3 sources per fact. Public-facing data claims should use at
least 2 authoritative external sources. Trusted voices on X are allowed as supporting
context, but not as the entire proof chain.

See:

- `nrg-bloom/content-engine/trust-policy.md`
- `nrg-bloom/content-engine/facts/public-data-registry-template.yaml`
- `nrg-bloom/content-engine/facts/public-market-facts-2026-03-26.yaml`

## First Goal

Beat generic content batches by making every output sound like:

- a builder talking to energy executives
- an operator talking to infrastructure investors
- a company with field proof, not borrowed confidence
