---
name: settlement-tracker
description: "Use this skill to track settlement negotiations -- offers, counter-offers, concessions, red lines, and negotiation dynamics across rounds. Trigger it whenever Makir asks about settlement status, the current offer gap, walk-away position, negotiation history, or concession strategy. Also trigger when settlement-related emails arrive from Dayo Adu, Marley Broda, TON counsel, or the mediator. Use during /status to populate the negotiation section. Use when Makir says 'where are we on settlement,' 'what did they offer,' 'should we accept,' 'update the tracker,' or when any new offer, counter-offer, or mediator proposal comes in. Also use when preparing for negotiation sessions to review what concessions remain available."
allowed-tools: Read, Write, Edit, Glob, Grep, mcp__google-workspace__gmail_users_messages_list, mcp__google-workspace__gmail_users_messages_get, mcp__google-workspace__gmail_users_threads_list, mcp__google-workspace__gmail_users_threads_get, mcp__memory__*
---

# Settlement Negotiation Tracker

## What This Skill Does

Maintain a real-time record of all settlement offers, counter-offers, concessions, and strategic positions across negotiation rounds. The skill exists because negotiations can stretch over weeks with multiple exchanges, and human memory is unreliable for tracking the precise evolution of positions, which concessions have been made, and what remains available to trade.

The walk-away floor ($500K USD) must always be visible in any output. This prevents the natural psychological drift that occurs during prolonged negotiations, where each incremental concession feels small but cumulatively erodes the position below an acceptable outcome.

## Evidence and File References

For the underlying evidence base that supports the negotiation position, see `references/evidence-inventory.md`.

## Negotiation File

Maintain at ~/Work/nrg-bloom/litigation-ton/settlement-tracker.yaml

### Schema

```yaml
last_updated: "YYYY-MM-DD"
matter: "NRG Bloom v. TON Infrastructure"
status: "active | paused | settled | failed"

framework:
  mechanism: "30-day negotiation -> 45-day mediation -> arbitration"
  start_date: "YYYY-MM-DD"
  negotiation_deadline: "YYYY-MM-DD"
  mediation_deadline: "YYYY-MM-DD"
  mediator: "Marley Broda (self-appointed) | [Neutral]"

parameters:
  nrg_bloom_opening: "$727,000 USD (N1.2B)"
  nrg_bloom_floor: "$500,000 USD"
  full_claim_range: "$1.1M-$2.4M USD (N1.8B-N4B)"
  mccarthy_litigation_range: "$1.6M-$6M+ USD"
  ton_estimated_zone: "$75K-$150K USD"

rounds:
  - round: 1
    date: "YYYY-MM-DD"
    type: "position_paper | counter_offer | negotiation_session | mediator_proposal"
    nrg_bloom:
      offer: "$X"
      key_arguments: ["list"]
      concessions_made: ["list"]
      new_evidence_deployed: ["list"]
    ton:
      offer: "$X"
      key_arguments: ["list"]
      concessions_detected: ["list"]
      new_arguments: ["list"]
    gap: "$X"
    assessment: "text"
    next_step: "text"

red_lines:
  - "Walk-away floor: $500K USD"
  - "No settlement without mutual release"
  - "No settlement without written acknowledgment of NRG Bloom contribution"
  - "No settlement that waives Axxela-related claims without adequate compensation"

concessions_available:
  - item: "Accept structured payment (50/50 over 90 days)"
    value: "Low -- timing concession only"
    deploy_when: "TON is close to floor but needs cash flow flexibility"
  - item: "Accept hybrid cash + ongoing revenue share"
    value: "Medium -- reduces upfront cash requirement"
    deploy_when: "TON can't pay lump sum but Axxela deal is active"
  - item: "Drop punitive damages claim"
    value: "Already excluded from settlement offer"
    deploy_when: "Already conceded in position paper"
  - item: "Narrow the claim to Axxela circumvention only"
    value: "High -- simplifies case but may reduce leverage"
    deploy_when: "Only if TON is close to $500K and wants to limit scope"

leverage_points:
  - "McCarthy Tetrault engagement (credible litigation threat)"
  - "Axxela circumvention email trail (undeniable documentary evidence)"
  - "Held-back WhatsApp evidence (impeachment ammunition)"
  - "Phoenix Trading prior lawsuit (pattern of conduct)"
  - "Axxela injunction threat ($15.3M deal at risk)"
  - "TON's need for Nigeria operations (can't afford full disclosure)"
```

## Process

1. **Load** settlement-tracker.yaml and query Memory MCP for latest negotiation context.
2. **Check Gmail** for new correspondence from Dayo, Marley, TON counsel, or the mediator.
3. **Compare** any new offer against the parameters -- especially the walk-away floor. The floor comparison is the first thing to check because everything else is irrelevant if the offer is below it.
4. **Update** the tracker YAML with new round data, offers, and any concessions observed.
5. **Present** the negotiation dashboard.

## Output Format

### Settlement Tracker -- [Date]

**Status**: [Active / Paused / X days remaining in negotiation window]

**Current Positions**
| Party | Latest Offer | Movement | % of NRG Bloom Claim |
|-------|-------------|----------|---------------------|
| NRG Bloom | $X | [+/- from previous] | 100% (baseline) |
| TON | $X | [+/- from previous] | X% |
| **Gap** | **$X** | | |

**Walk-Away Check**: [ABOVE FLOOR / BELOW FLOOR / AT FLOOR]

**Round History**
| Round | Date | NRG Offer | TON Offer | Key Development |
|-------|------|-----------|-----------|----------------|

**Concessions Made**
- NRG Bloom: [list]
- TON: [list]

**Concessions Available** (not yet deployed)
- [item] -- Deploy when: [condition]

**Red Lines** (non-negotiable)
- [list]

**Recommended Next Move**
- [Strategic recommendation based on current positions, dynamics, and available leverage]

## Stalling and Deadline Detection

Flag these patterns proactively because they indicate the negotiation may be failing:
- **No movement across 2+ rounds**: TON may be stalling to run out the clock or to wear down NRG Bloom's resolve.
- **Negotiation window approaching expiry**: Surface the countdown prominently so Makir can decide whether to extend, escalate to mediation, or proceed to arbitration.
- **Mediator bias signals**: If the mediator (currently Marley Broda, who is self-appointed and not neutral) consistently pushes concessions on NRG Bloom without equivalent pressure on TON, flag this as a process concern.

After each round, update Memory MCP with the latest positions so the next session starts with current context.

All content is confidential and privileged. Negotiation positions and strategy are among the most sensitive information in the dispute -- they should not appear in any output that could be shared externally.
