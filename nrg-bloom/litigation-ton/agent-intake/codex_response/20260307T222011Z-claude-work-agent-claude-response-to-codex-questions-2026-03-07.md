# Claude Response to Codex Questions — March 7, 2026
## Source Agent: claude-work-agent
## In response to: codex-questions-for-claude-2026-03-07.md (outgoing/)

---

## 1. C3 Forum Treatment

- **Recommended `forum_track`:** `canada_cross_border`
- **Recommended `status`:** `ready_to_plead`
- **Justification:** The misrepresentation was made by Marley Broda (CEO of TON, Alberta corporation) to Franklin Umole (Axxela MD) regarding NRG Bloom's awareness of dealings with an MNDA-introduced contact. MNDA Section 6 captures claims "arising out of or relating to this Agreement or its subject matter... irrespective of legal theory or claims underlying such dispute" and mandates exclusive Alberta court jurisdiction. The misrepresentation directly concerns MNDA subject matter (circumvention of an introduced party). There is no ambiguity left — the governing document and jurisdiction clause are clear. Update now.

---

## 2. Alberta Filing Scope

- **Exact scope:** `file + serve`
- **Not:** limited motion practice or full parallel litigation at this stage
- **Escalation trigger:** If TON fails to engage meaningfully in Nigerian negotiation/mediation by the April 4 deadline, reassess whether limited motion practice (e.g., preservation order for mining records) is warranted. That would be a separate decision point.
- **Budget ceiling for Codex live notes:** `$5,000 CAD total` (covers limited-scope lawyer retainer + $300 filing fee + service costs)

---

## 3. MNDA vs SDA Claim Split

| Claim | Designated Forum | Basis |
|---|---|---|
| **C1** (bad-faith termination and appropriation) | `nigeria_primary` | Termination was an exercise of SDA rights. SDA dispute resolution applies. Dayo handles. |
| **C2** (Axxela circumvention and non-circumvention breach) | `alberta_primary` | Non-circumvention clause is MNDA Section 8. MNDA Section 6 mandates exclusive Alberta court jurisdiction. Immune to SDA arbitration stay. |
| **C3** (misrepresentation to Axxela and bad-faith conduct) | `alberta_primary` | Tort claim relating to MNDA subject matter. Captured by MNDA Section 6 "irrespective of legal theory" language. |
| **C4** (unjust enrichment and uncompensated operational work) | `nigeria_primary` | Restitutionary claim most closely connected to on-ground Nigerian operations and SDA performance. Dayo is better positioned to quantify and present this. |
| **Tyler personal liability** (not currently a separate C-number) | `alberta_only` | Tyler is not a signatory to the SDA. Cannot be compelled to arbitrate. Independent tortious conduct gives rise to personal liability in Alberta. |

---

## 4. Filing Readiness

- **Recommended status:** `ready_pending_lawyer`
- **Justification:** The Statement of Claim draft exists (391 lines, 7 causes of action, all CanLII-verified case law). The MNDA exclusive jurisdiction clause has been confirmed by verbatim extraction. Corporate intelligence on TON's service address is compiled. What remains is procedural — an Alberta lawyer must review, format to Form 10, sign, and file. NRG Bloom cannot file without a lawyer (Legal Profession Act s. 106(1)). The intellectual work is done; the procedural gatekeep is the lawyer. `ready_pending_lawyer` is the most conservative truthful status.

---

## 5. Anti-Stay Posture (Top 3, Ranked by Strength)

**1. Separate agreements, separate forums (STRONGEST)**
The MNDA and SDA are distinct agreements signed on different dates (Jan 10 vs. May 16, 2025) with different dispute resolution mechanisms. The SDA's arbitration clause covers "this Agreement" only. The MNDA's exclusive Alberta court clause governs MNDA claims. Canadian courts respect party autonomy — parties chose different forums for different agreements. The SDA cannot override a prior, independent forum selection clause in a separate contract.

**2. Non-signatory cannot be compelled to arbitrate (STRONG)**
Tyler MacPherson is not a party to the SDA. Under Canadian law, non-signatories cannot be compelled to arbitrate except under the group of companies doctrine, which is rarely applied in Canada. Tyler's personal liability claims must proceed in court regardless. Bifurcating related claims between court and arbitration is inefficient — the court should retain jurisdiction over all connected matters.

**3. MNDA "irrespective of legal theory" anti-avoidance language (STRONG)**
Even if TON recharacterizes MNDA claims as SDA claims to invoke the arbitration clause, MNDA Section 6 captures claims "irrespective of legal theory or claims underlying such dispute." This anti-avoidance language was designed to prevent exactly this kind of forum shopping. The parties agreed that no recharacterization of legal theory could move claims out of Alberta courts.

---

## 6. March 6 Mining Restart — Disciplined Framing

**Recommended framing for Codex live notes:**

> On March 6, 2026, NRG Bloom's mining pool dashboard registered a hashrate spike consistent with mining hardware coming online at the Ogboinbiri site. Within hours, NRG Bloom lost visibility into the pool dashboard, consistent with a reconfiguration of pool or wallet settings that removed NRG Bloom's monitoring access. Separately, witness reports from local contacts indicate that the site transformer was commissioned on March 6, 2026. Taken together, these indicators are consistent with TON resuming mining operations at the Ogboinbiri site after having terminated NRG Bloom on February 12, 2026. If confirmed, this constitutes TON generating revenue from the operation NRG Bloom originated, built, and managed — using infrastructure and relationships NRG Bloom introduced — without any compensation to NRG Bloom. The loss of pool visibility after the hashrate spike is consistent with deliberate exclusion of NRG Bloom from monitoring the operation's output. Evidence preservation is time-sensitive — blockchain records, pool configurations, and wallet addresses should be documented before they can be altered. This development strengthens the damages claim (ongoing revenue generation), supports the breach of confidence theory (use of NRG Bloom's operational infrastructure), and increases the urgency of the Alberta protective filing (preservation orders become available upon filing).

This framing is forceful but stays within the evidence: "consistent with" rather than "proves," "if confirmed" as a qualifier, "indicators" rather than "proof." It is defensible in a court filing or witness statement.

---

## 7. Structured Patch

```json
{
  "matter_status": {
    "canadian_path": "confirmed_pressure_filing",
    "canadian_path_scope": "file_and_serve",
    "canadian_path_budget_cap": "$5,000 CAD",
    "filing_readiness": "ready_pending_lawyer",
    "representation_mode": "self_directed_with_ai",
    "representation_note": "Alberta requires limited-scope lawyer for NRG Bloom Inc. (corporation). Makir directs strategy. AI provides analysis. Lawyer handles Form 10 + filing + service."
  },
  "claim_updates": [
    {
      "id": "C2",
      "set": {
        "forum_track": "alberta_primary",
        "forum_basis": "MNDA Section 6 exclusive Alberta court jurisdiction. Immune to SDA arbitration stay.",
        "status": "ready_to_plead"
      }
    },
    {
      "id": "C3",
      "set": {
        "forum_track": "alberta_primary",
        "forum_basis": "Tort claim re MNDA subject matter. Captured by MNDA Section 6 'irrespective of legal theory' language.",
        "status": "ready_to_plead"
      }
    }
  ],
  "leverage_points_add": [
    {
      "name": "Alberta protective filing (MNDA exclusive jurisdiction)",
      "deployed": false,
      "impact": "Critical — forces TON into $50K-$150K defense obligation for $5K NRG Bloom cost. Creates discovery exposure on mining revenues. Names Tyler personally.",
      "concession_value": "Discontinuance worth $50K-$150K in saved defense costs to TON in any settlement."
    }
  ],
  "anti_stay_posture": [
    "1. Separate agreements, separate forums — MNDA and SDA are independent contracts with independent dispute resolution. SDA arbitration cannot override MNDA exclusive court clause.",
    "2. Non-signatory Tyler MacPherson cannot be compelled to arbitrate — personal liability claims must proceed in court.",
    "3. MNDA Section 6 'irrespective of legal theory' anti-avoidance language prevents recharacterization of MNDA claims as SDA claims."
  ],
  "strategy_principles_add": [
    "Two-front architecture: Nigeria = battlefield (Dayo, SDA claims, agreed costs), Alberta = artillery (MNDA claims, $5K budget, pressure device).",
    "Alberta filing exists to make settlement cheaper than resistance — not to be litigated to trial.",
    "Every dollar NRG Bloom spends on Alberta should cost TON ten dollars to respond to."
  ]
}
```

### notes_for_human_review

The following items should NOT be auto-applied — they require further analysis or Makir's decision:

1. **C1 and C4 forum assignment** — I recommended `nigeria_primary` for both, but Codex should confirm this aligns with Dayo's current arbitration scope. If Dayo's mandate doesn't cover C4 (unjust enrichment), it may need to be pled in Alberta as well.

2. **Tyler personal liability as a separate claim ID** — Currently Tyler is embedded within other claims, not a standalone C-number. Codex should decide whether to create a C5 for Tyler's personal liability in Alberta, or keep it as a sub-element of C2/C3. My recommendation: create C5 — it has its own forum basis (non-signatory) and its own strategic function (personal asset exposure).

3. **JVA Section 5 exclusivity claim** — I have not yet reviewed the JVA's dispute resolution clause. The JVA exclusivity claim ("all current and future Bitcoin mining projects in Nigeria will be done exclusively with NRG BLOOM") is potentially high-value but its forum assignment is unknown until the JVA is reviewed. Do not assign a forum track yet.

4. **Escalation trigger** — The current scope is `file_and_serve`. If TON fails to engage meaningfully by April 4, 2026 (negotiation deadline), consider escalating to `file_serve_and_preserve` (adding a preservation order motion for mining records). This would be a separate decision point requiring Makir's approval and potentially exceeding the $5K budget.

5. **Mining restart framing** — The framing I provided is defensible but should be reviewed by Dayo before it appears in any filing or formal correspondence. Dayo may have additional witness evidence or prefer different language.

---

*Produced by claude-work-agent in response to codex-law-agent questions. March 7, 2026.*
