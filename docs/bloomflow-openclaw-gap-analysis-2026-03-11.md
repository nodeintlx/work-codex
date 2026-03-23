# BloomFlow OpenClaw Gap Analysis

Created: 2026-03-11
Source input: `bloomflow-openclaw-integration.docx` from `/mnt/c/Users/volcy/Downloads`

## What The Downloaded V2 Spec Wants

The downloaded document defines BloomFlow as a three-layer autonomous system:

1. Intelligence layer
   - `bloom-btc-watch`
   - `bloom-energy-watch`
   - `bloom-africa-watch`
   - `bloom-ai-infra-watch`
2. Decision layer
   - `bloom-signal-router`
3. Production layer
   - `bloom-intake`
   - `bloom-run`
   - `bloom-creative`
   - `bloom-workflow`

It also assumes:

- OpenClaw skill execution on a VPN-isolated VPS
- trigger and approval flow through Telegram, Slack, or WhatsApp
- continuous polling and signal scoring
- autonomous generation with human approval before scheduling/publishing

## What Already Exists In This Repo

BloomFlow already has a strong production core:

- canonical content brief model
- queue and editorial board
- copy generation
- creative direction generation
- workflow state transitions
- backend summary JSON
- frontend contract JSON

This means the repo already covers a large part of the production layer.

## Current Mapping

### Production Layer

Desired skill
Current repo status
Notes

`bloom-intake`
implemented
`content-intake` creates canonical briefs and queue items

`bloom-run`
partially implemented
split today across `content-draft` and `content-creative`

`bloom-creative`
implemented
`content-creative`

`bloom-workflow`
implemented
`content-editorial`, `content-status`, `content-backend`, `content-app`

### Decision Layer

Desired skill
Current repo status
Notes

`bloom-signal-router`
not yet implemented
no signal scoring or auto-fire logic yet

### Intelligence Layer

Desired skill
Current repo status
Notes

`bloom-btc-watch`
not implemented
no market polling in repo yet

`bloom-energy-watch`
not implemented
no energy feeds or flare/regulation monitors yet

`bloom-africa-watch`
not implemented
no Africa/Nigeria news ingestion yet

`bloom-ai-infra-watch`
not implemented
no AI/data-center news ingestion yet

## Critical Missing Runtime Pieces

To match the downloaded v2 spec, BloomFlow still needs:

1. watch agents with polling schedules
2. a signal router with thresholds and cooldowns
3. messaging-channel command handling
4. approval loop over Telegram or equivalent
5. scheduling daemon and publish executor
6. source adapters for APIs, RSS, and web search

## Immediate Build Order

The right order is:

1. formalize the command contract for messaging channels
2. define the signal report schema
3. implement the signal router
4. implement one watcher first, not all four
5. connect the router to the existing BloomFlow production commands
6. add messaging approval flow

## Recommendation

Start with the narrowest viable autonomous path:

- one watcher: `bloom-ai-infra-watch`
- one signal router
- one message channel: Telegram
- one action: generate content brief and package for approval

That proves the architecture before the system gets spread across four intelligence domains.
