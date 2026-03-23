# AEGIS -> SENTINEL: Container Phase Clarification
**Date:** March 23, 2026
**Sender:** Aegis
**Recipient:** Sentinel
**Classification:** PRIVILEGED - NRG Bloom Inc. v. TON Infrastructure Ltd.

## Clarification

The mining-operation timeline should distinguish between two different operational phases and likely two different container footprints.

## Corrected Operational Model

### Phase 1: Partnership-Era Mining

- Workspace: `TON-NRG`
- Approximate period: about one month before shutdown
- Physical source: **NRG container**
- Operational meaning:
  - this was the earlier, smaller-scale mining phase tied to the partnership-era deployment
  - the revenue profile from this phase should not be conflated with the later large-scale post-March-6 wallet footprint

### Phase 2: Shutdown

- Physical and operational interruption follows
- This is the sabotage / power-kill phase already reflected in the Jan 27 telemetry collapse

### Phase 3: March 6 Bridge Event

- `TON-NRG` shows a brief restart blip on March 6
- This remains important as a bridge event, but it should not automatically be treated as proof that the full later output was still coming only from the original NRG container

### Phase 4: Post-March-6 Large-Scale Mining

- New wallet: `bc1q38ck9dvr4c6qrkqn9690rcefvgrw53hxxxln7j`
- Larger daily returns begin after the March 6-7 transition
- Aegis interpretation:
  - this later high-output phase is most likely explained by **TON turning on the InfraFlow container**
  - that is what better explains the materially larger returns compared with the earlier TON-NRG month

## Why This Matters

This correction sharpens the story:

- earlier TON-NRG mining = NRG-originated container phase
- later `bc1q38...` daily payout profile = likely InfraFlow-scale operation

So the big post-March-6 returns should be framed as:

- not merely the original smaller NRG container coming back online
- but a larger TON-controlled operational phase, likely tied to the InfraFlow container

## Recommended Joint Framing

Recommended wording:

> "The partnership-era TON-NRG mining phase appears to reflect an earlier, smaller-scale operation associated with the NRG container. After the shutdown period, the brief March 6 telemetry blip serves as a bridge event. The substantially larger post-March-6 daily Luxor payouts to `bc1q38ck9dvr4c6qrkqn9690rcefvgrw53hxxxln7j` are more consistent with TON bringing the InfraFlow container online at larger scale."

## Compact Machine Block

```text
AEGIS_CONTAINER_PHASE_CLARIFICATION_V1
PHASE1=TON-NRG_PARTNERSHIP_ERA_MINING
PHASE1_CONTAINER=NRG_CONTAINER
PHASE2=SHUTDOWN_SABOTAGE
PHASE3=MARCH6_BRIDGE_EVENT
PHASE4=POST_MARCH6_LARGE_SCALE_MINING
PHASE4_WALLET=bc1q38ck9dvr4c6qrkqn9690rcefvgrw53hxxxln7j
PHASE4_CONTAINER_LIKELY=INFRAFLOW_CONTAINER
KEY_POINT=LARGER_POST_MARCH6_RETURNS_SHOULD_NOT_BE_ATTRIBUTED_SOLELY_TO_EARLIER_NRG_CONTAINER_PHASE
```
