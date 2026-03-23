# Sentinel Update: Full Session Summary — March 9, 2026

## Source Agent: Sentinel | Date: March 9, 2026
## Classification: CONFIDENTIAL — LITIGATION WORK PRODUCT

---

## SESSION OVERVIEW

Major developments across evidence, legal team, and case preparation. Court proceedings expected to begin this week.

---

## 1. NEW EVIDENCE — KADIO X VIDEO (Critical)

On March 7, 2026, **Kadio** (associate of Yakubu Tanimu and Oladipo "Ola" Olaniyan) posted a video on X (Twitter) showing people working inside the **Infraflow container** (TON's 40' power distribution container) at the Ogboinbiri site.

**URL:** https://x.com/kadio_b/status/2030410616515510698

**Corroboration:** Claudy D Claudius (former full-time NRG Bloom employee) identified other individuals in the video as **security agents previously employed by NRG Bloom**.

### What This Proves
1. **TON-Ola post-termination coordination** — Kadio is Ola's associate, operating inside TON's Infraflow
2. **Jeff Jespersen's termination call statements are provably false:**
   - Denied engaging with Ola/Nelson — contradicted by video
   - "We've been told that they don't even want to take it" — implies communication with Ola
   - "The container belongs to Ola" — admission of Ola's involvement
3. **NRG Bloom's own staff co-opted** — former security agents now working for TON/Ola
4. **Mining restart confirmed** — video posted Mar 7, consistent with Mar 6 hashrate spike observation
5. **Manufactured termination sequence complete:** Ola sabotages (Jan 27) → TON terminates citing non-operational (Feb 12) → TON partners with Ola to resume mining using NRG Bloom's staff (Mar 6-7)

### Evidence Preservation Status
- **COMPLETED:** Julie Peeters emailed full evidence package to Dayo Adu on March 8, 2026
- Attachments sent: kadio video.mp4, termination call screenshots (3), infraflow_inside.jpg, dashboard_march_7_2026.png, claudy_message_march_8_2026.jpg
- Email is in the Dayo thread (Subject: "Re: 25-101-01 - Ogboinbiri - Position Summary Document")

---

## 2. LEGAL TEAM EXPANSION

Dayo Adu has expanded the Moroom Africa team from 2 to 4 lawyers:

| Name | Role | Email | Specialty |
|------|------|-------|-----------|
| **Dayo Adu** | Lead Counsel | dayo.adu@moroomafrica.com | Managing Partner, IBA network |
| **Jane Ibikunle** | Associate | jane@moroomafrica.com | Evidence review, Drive access |
| **Mercy Airiohuodion** | Senior Associate (NEW) | mercy.airiohuodion@moroomafrica.com | Dispute Resolution (primary), Energy sector, Nigerian Bar 2014, Chambers contributor |
| **Joshua Adedokun** | Executive Associate (NEW) | joshua.adedokun@moroomafrica.com | Support — research, document prep, court filing coordination |

### Assessment
- **Mercy is the key addition.** Dispute resolution lead + energy sector background = likely technical lead on the injunction application.
- **Staffing up from 2 to 4 signals Dayo is preparing for active court proceedings**, not just negotiation or mediation.
- All 4 lawyers have been sent the full chronology and complete email record (see below).

---

## 3. DOCUMENTS DELIVERED TO LEGAL TEAM

Two comprehensive documents compiled and sent to all 4 Moroom Africa lawyers:

### a) Complete Chronology
- **File:** chronology-nrg-bloom-v-ton-2026-03-09.md
- **Drive:** https://drive.google.com/file/d/1pCb_KLxA-8b8xQH8IAFokjVK2X1x1eu0/view
- **Scope:** Feb 4, 2025 — Mar 9, 2026 (14 months)
- **Contents:** 11 phases, every significant dated event with evidence source citations
- **Includes:** Key parties table, asset identification (Infraflow = 40' container, 20' from Canada = miners/equipment, NRG Bloom's 20' = separate), progressive diminishment summary, manufactured termination sequence
- **Verified against source files** — corrections applied for container identification, dates, and amounts

### b) Complete Email Record
- **File:** ton-emails-complete-record-2026-03-09.md
- **Drive:** https://drive.google.com/file/d/1KgKHzV0r827MBAEiikHaQvaLKphAhiNU/view
- **Total:** 199 emails, Jan 9, 2025 — Mar 6, 2026
- **Size:** 1.5 MB / 37,310 lines
- **Format:** Chronological, full headers (From/To/CC/Date/Subject), complete body text, attachment filenames, Gmail IDs preserved
- **Participants:** 16 unique senders including all TON personnel, NRG Bloom team, Dayo, Axxela contacts
- **Zero fetch errors, zero decode errors**

---

## 4. DAYO STRATEGY CALL — MARCH 9

Dayo texted Makir on March 8: "We can't rush the next steps at all. Trust me that we will get our injunction. I'll call tomorrow to elaborate on the strategy."

**Call is today (March 9).** Key questions:
1. Injunction type — interim, interlocutory, or Mareva/freezing?
2. Which court — Federal High Court Lagos? State High Court?
3. Filing timeline
4. Whether the Kadio video evidence will be included in the application
5. What Makir needs to provide
6. Cost estimate
7. Alberta filing coordination and sequencing

**Court proceedings expected to begin this week (March 9-13).**

---

## 5. CONTAINER IDENTIFICATION — CORRECTED

Previous communications may have been imprecise on container identification. Corrected definitions:

| Asset | Description |
|-------|-------------|
| **Infraflow (40' container)** | TON's power distribution/infrastructure container. Shipped from Canada, arrived Lagos Jul 16, 2025. Arrived Yenagoa late Sep/early Oct 2025. This is what Kadio's video shows. |
| **20' container from Canada** | TON's mining container with 95 ASIC miners and equipment. Shipped Jul 22, 2025. Arrived Bayelsa Oct 7-8, 2025. |
| **NRG Bloom's 20' container** | Pre-existing NRG Bloom container at Ogboinbiri. 33 miners (Agnes/Nelson proof of concept). Separate from TON's containers. |

---

## 6. JEFF JESPERSEN CREDIBILITY — COMPROMISED

Jeff Jespersen's credibility is now formally compromised by three contradicted statements on the February 12, 2026 termination call:

| Statement | Contradicted By |
|-----------|----------------|
| Denied TON would engage with Ola or Nelson | Kadio (Ola's associate) working inside Infraflow — video evidence |
| "We've been told that they don't even want to take it" | Implies active communication with Ola at time of termination |
| "The container belongs to Ola" | Admission of Ola's involvement with TON's infrastructure |

**Impeachment value:** If Jeff or Marley ever testify that TON had no relationship with Ola post-termination, this video is devastating.

---

## 7. INFRASTRUCTURE FIXES

**gws Drive upload pattern corrected.** Previous uploads to Aegis incoming/ folder were silently going to Drive root because `--params` was being used for file metadata. The fix:

- **Correct:** `gws drive files create --json '{"name": "file.md", "parents": ["FOLDER_ID"]}' --upload /path/to/file`
- **Wrong:** `gws drive files create --params '{"name": "file.md", "parents": ["FOLDER_ID"]}' --upload /path/to/file`

`--json` = request body metadata (name, parents). `--params` = URL query parameters only. This is documented in rules and reference files for all future sessions.

---

## RECOMMENDED AEGIS STATE UPDATES

```json
{
  "matter_status": {
    "phase": "active_court_proceedings",
    "nigerian_proceedings": "injunction_application_in_preparation — court process beginning week of March 9-13",
    "negotiation_status": "CLOSED",
    "alberta_filing": "ON HOLD pending Dayo call March 9"
  },
  "legal_team": {
    "firm": "Moroom Africa LLP",
    "lead": "Dayo Adu (Managing Partner)",
    "team": [
      "Dayo Adu — lead counsel",
      "Jane Ibikunle — associate, evidence review",
      "Mercy Airiohuodion — Senior Associate, dispute resolution lead, energy sector (NEW Mar 9)",
      "Joshua Adedokun — Executive Associate, support (NEW Mar 9)"
    ],
    "team_size": 4,
    "expansion_signal": "Staffing up from 2 to 4 = preparing for active court proceedings"
  },
  "evidence_register_update": {
    "E-VIDEO-001": {
      "status": "DELIVERED_TO_COUNSEL",
      "delivered_by": "Julie Peeters, Mar 8, 2026",
      "attachments": ["kadio video.mp4", "termination_call screenshots (3)", "infraflow_inside.jpg", "dashboard_march_7_2026.png", "claudy_message_march_8_2026.jpg"]
    }
  },
  "documents_delivered": {
    "chronology": {
      "file": "chronology-nrg-bloom-v-ton-2026-03-09.md",
      "drive_url": "https://drive.google.com/file/d/1pCb_KLxA-8b8xQH8IAFokjVK2X1x1eu0/view",
      "scope": "Feb 4, 2025 — Mar 9, 2026",
      "status": "sent_to_all_4_lawyers"
    },
    "email_record": {
      "file": "ton-emails-complete-record-2026-03-09.md",
      "drive_url": "https://drive.google.com/file/d/1KgKHzV0r827MBAEiikHaQvaLKphAhiNU/view",
      "total_emails": 199,
      "period": "Jan 9, 2025 — Mar 6, 2026",
      "status": "sent_to_all_4_lawyers"
    }
  },
  "jeff_jespersen_credibility": "COMPROMISED — 3 termination call statements contradicted by public video evidence",
  "container_identification_corrected": {
    "infraflow_40ft": "Power distribution container — arrived Yenagoa late Sep/early Oct 2025. Shown in Kadio video.",
    "20ft_from_canada": "Mining container with 95 ASIC miners — arrived Bayelsa Oct 7-8, 2025.",
    "nrg_bloom_20ft": "Pre-existing NRG Bloom container, 33 miners, separate from TON assets."
  },
  "live_notes_append": "March 9: Major session. Kadio video evidence documented and delivered to counsel. Legal team expanded to 4 (Mercy Airiohuodion = dispute resolution lead, Joshua Adedokun = support). Full chronology (verified, corrected) and 199-email record compiled and sent to all lawyers. Court proceedings beginning this week. Dayo strategy call today.",
  "live_next_actions_update": [
    "PRIORITY 1: Debrief Dayo call — injunction type, court, timeline, evidence package needs",
    "PRIORITY 2: Update Sentinel + Aegis with call outcomes",
    "PRIORITY 3: Coordinate Alberta filing timing with Nigerian injunction",
    "PRIORITY 4: If Dayo requests additional evidence or documents, compile immediately",
    "PRIORITY 5: Establish direct communication channel with Mercy for day-to-day court filing updates"
  ]
}
```

---

*Produced by Sentinel. March 9, 2026. For ingestion by Aegis. Upload to incoming/.*
