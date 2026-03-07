# Canadian Litigation Self-Study Roadmap
## NRG Bloom Inc. v. TON Infrastructure Ltd. — AI-Powered Self-Representation

**Created**: March 6, 2026
**Purpose**: Practical playbook for navigating the Canadian legal system as a self-represented litigant (SRL) using AI tools
**Jurisdiction**: Alberta, Canada (Court of King's Bench)
**Status**: Living document — update as you learn

---

## Table of Contents

1. [Phase 0: The Critical Decision — Arbitration vs. Court](#phase-0)
2. [Phase 1: Limitation Period — Protect Your Rights NOW](#phase-1)
3. [Phase 2: Forum Selection & Filing Mechanics](#phase-2)
4. [Phase 3: Your Legal Theories — The Substance](#phase-3)
5. [Phase 4: Evidence Rules — Getting Your Proof Admitted](#phase-4)
6. [Phase 5: AI in Canadian Courts — Rules of Engagement](#phase-5)
7. [Phase 6: Costs & Risk Management](#phase-6)
8. [Phase 7: Service on International Parties](#phase-7)
9. [Phase 8: Tools & Resources for SRLs](#phase-8)
10. [Study Sequence — What to Learn First](#study-sequence)

---

<a name="phase-0"></a>
## Phase 0: The Critical Decision — Arbitration vs. Court

### The Section 7 Question

Your agreements contain an arbitration clause (Section 7). This is the **first strategic decision** you need to make, because it determines everything else.

### Two Governing Statutes in Alberta

| Statute | Applies When |
|---------|-------------|
| **Arbitration Act** (RSA 2000, c A-43) | Domestic disputes between Canadian parties |
| **International Commercial Arbitration Act** | One party is international (TON = Nigerian-connected) |

Alberta's International Commercial Arbitration Act adopts the **UNCITRAL Model Law** and implements the **New York Convention** for enforcement of foreign arbitral awards. Canada was the **first country in the world** to enact legislation implementing the Model Law (1986).

### The Mandatory Stay Problem (Section 7(1))

**CRITICAL**: Under s. 7(1) of the Arbitration Act, if you file in court and TON has an arbitration clause, TON can apply to **stay your court action** and force arbitration.

> "If a party to an arbitration agreement commences a proceeding in court in respect of a matter in dispute to be submitted to arbitration under the agreement, **the court shall, on the application of another party**, stay the proceeding."

The court can **only refuse** a stay if:
- (a) A party was under legal incapacity when signing
- (c) The subject matter is not capable of arbitration
- (d) **The stay application was brought with undue delay**
- (e) The matter is proper for default or summary judgment

### How to Avoid Being Forced to Arbitrate

Key arguments to resist a stay:

1. **Scope limitation** — Does Section 7 cover ALL your claims, or only some? If your claims (e.g., tortious interference, breach of confidence) fall **outside** the scope of the arbitration clause, the court may hear those claims.

2. **Waiver/participation** — If TON has participated in any court-like proceedings (e.g., the mediation) without insisting on arbitration, they may have **waived** their right. Case: *Agrium v. Orbis Engineering* (2022 ABCA 266) — failing to move promptly and participating in litigation can constitute waiver.

3. **Void, inoperative, or incapable of being performed** — Per SCC in *Peace River Hydro Partners v. Petrowest Corp.*, the resisting party bears the onus, and scope is interpreted **narrowly**.

4. **Third-party beneficiary limitation** — *Husky Oil v. Technip* (2024 ABCA 369) held that arbitration clauses don't bind third parties unless the requirement is "manifest and expressed in clear and explicit language."

### Strategic Analysis: Arbitration vs. Court for an SRL

| Factor | Arbitration | Court |
|--------|------------|-------|
| **Cost** | Expensive (arbitrator fees $300-500/hr, venue, admin) | Cheaper (filing fee ~$250, no arbitrator to pay) |
| **Procedural complexity** | Simpler rules, more flexible | Formal Rules of Court apply |
| **SRL-friendliness** | Less — arbitrators expect sophistication | More — courts accommodate SRLs |
| **Discovery/disclosure** | Limited | Full Affidavit of Records |
| **Appeal rights** | Very limited | Available |
| **Enforcement** | Need court to enforce award anyway | Direct enforcement |
| **International enforcement** | New York Convention (strong) | May need foreign court recognition |
| **Speed** | Potentially faster | 36-month target (new 2025 rules) |

**Recommendation**: Court is likely more favorable for an SRL — lower cost, more accommodating of self-representation, broader discovery rights (you want full disclosure from TON), and stronger appeal rights. But be prepared for the Section 7 stay application.

### Key Reading

- Alberta Arbitration Act: [CanLII](https://www.canlii.org/t/822r)
- Alberta International Commercial Arbitration Act: [Open Alberta](https://open.alberta.ca/publications/i05)
- *Husky Oil v. Technip* (2024 ABCA 369) — third-party arbitration limits
- *Agrium v. Orbis* (2022 ABCA 266) — waiver and delay
- *Peace River Hydro Partners v. Petrowest Corp.* (SCC) — mandatory stay prerequisites

---

<a name="phase-1"></a>
## Phase 1: Limitation Period — Protect Your Rights NOW

### This Is Time-Sensitive

Alberta follows the **2/10 rule** under the Limitations Act (RSA 2000, c L-12):

| Period | Rule | What It Means |
|--------|------|--------------|
| **2 years** | Discovery rule — starts when you **knew or ought to have known** | Clock starts when you can draw a "plausible inference" of liability |
| **10 years** | Ultimate limitation — from the date of the wrongful act | Cannot be extended regardless of discovery |

### When Did YOUR Clock Start?

The "discovery rule" requires all three elements:
1. You knew (or should have known) an **injury occurred**
2. The injury was **attributable to TON's conduct**
3. The injury **warrants commencing an action**

**The "plausible inference" standard** (from *Grant Thornton LLP v. New Brunswick*): You don't need certainty. Once you could reasonably infer TON was liable, the 2-year clock started.

**Your fact pattern**: You need to identify the earliest date you had enough information to draw a plausible inference of breach. This could be:
- The date TON cut you out of the Axxela deal
- The date you discovered circumvention activity
- The date of the last significant breach in a continuing course of conduct

**Important**: For a **continuing course of conduct** or series of related acts/omissions, the claim arises when the conduct **terminates** or the **last act or omission occurs**. This could extend your window if TON's breaches were ongoing.

### Preserving Your Limitation Period — Protective Filing

You can file a Statement of Claim **solely to stop the clock**, even if you're not ready to fully prosecute:

1. **Prepare a Statement of Claim** (Form 10) — it doesn't need to be perfect, but must set out the material facts
2. **File it** at the Court of King's Bench ($250 fee, in-person for SRLs)
3. **You have 1 year to serve it** on the defendant after filing
4. If you don't serve within 1 year, you're **barred from recovery** (but can apply for extension BEFORE the deadline)

This is your safety net. File first, refine later.

### Key Exceptions That Pause the Clock

- **Fraud**: If TON concealed the injury, the limitation period can be **suspended**
- **Continuing wrong**: If the breaches are part of an ongoing course of conduct, the clock may run from the last act

### Action Items

- [ ] **Determine your earliest discovery date** — when could you first draw a plausible inference?
- [ ] **Calculate your 2-year deadline** from that date
- [ ] **If the deadline is approaching, file a protective Statement of Claim immediately**
- [ ] **Budget $250** for the filing fee (or apply for fee waiver)

### Key Reading

- Alberta Limitations Act: [CanLII](https://www.canlii.org/en/ab/laws/stat/rsa-2000-c-l-12/)
- [Primer on Limitation Periods in Alberta](https://wt.ca/a-primer-on-limitation-periods-in-alberta/)
- [Grant Thornton — When Does the Clock Start?](https://www.millerthomson.com/en/insights/commercial-litigation/limitation-period-trigger-alberta/)

---

<a name="phase-2"></a>
## Phase 2: Forum Selection & Filing Mechanics

### Alberta Court of King's Bench — How to File

| Item | Detail |
|------|--------|
| **Court** | Court of King's Bench of Alberta |
| **Jurisdiction** | Claims exceeding $50,000 (yours is well above) |
| **Form** | Statement of Claim — Form 10 |
| **Filing fee** | ~$250 (updated May 14, 2025 — verify at [alberta.ca/court-fees](https://www.alberta.ca/court-fees)) |
| **Filing method** | **In-person for SRLs** at Clerk's Office filing counters (lawyers can file by email) |
| **Counter hours** | Until 4:00 PM every weekday |
| **Service deadline** | Must serve defendant **within 1 year** of filing |
| **Fee waiver** | Available — apply at [alberta.ca/waive-filing-fee](https://alberta.ca/waive-filing-fee) |

### What Must Be in Your Statement of Claim

1. **Who** is making the claim (NRG Bloom Inc., through you as director/representative)
2. **Who** the claim is against (TON Infrastructure Ltd., potentially Tyler MacPhearson personally)
3. **The alleged facts** — material facts relevant to each cause of action
4. **The relief sought** — specific damages amounts, declaratory relief, constructive trust, etc.

### NEW 2025 Requirement: Mandatory Litigation Plans

**Effective September 1, 2025**, all actions commenced by Statement of Claim require:

- **Litigation Plan filed within 4 months** from service of the first Statement of Defence
- **Civil Trial Target**: matters should resolve or proceed to trial within **36 months**

Key deadlines from the "Trigger Date" (first Statement of Defence):
- 8 months — Third-party pleadings complete
- 10 months — Disclosure of records complete
- 12 months — Witness lists complete
- 25 months — Questioning of witnesses adverse in interest
- 33 months — Expert reports + ADR participation

> "Actions shall no longer move through the system at a self-directed, voluntary pace."

### Electronic Filing

| System | Court | SRL Access |
|--------|-------|-----------|
| **KB Filing Digital Service** ([qb-filing.alberta.ca](https://qb-filing.alberta.ca)) | King's Bench | Currently for lawyers/legal assistants only |
| **CAMS** ([cams.albertacourts.ca](https://cams.albertacourts.ca)) | Court of Appeal | SRLs with active matters can register |

As an SRL, you'll likely need to file **in person** at the King's Bench registry.

### Forms & Templates

- [Civil Forms — Court of King's Bench](https://www.albertacourts.ca/kb/areas-of-law/civil/forms)
- [Court Procedure Booklet for SRLs](https://www.alberta.ca/system/files/jus-making-court-application-court-kb-with-claim-form.pdf)
- [Alberta Law Libraries — Finding Forms](https://lawlibrary.ab.ca/navigating-legal-information/find-forms-and-precedents/)
- [LawCentral Alberta](https://www.lawcentralalberta.ca/en/preparing/accessing-law-related-and-court-forms)

---

<a name="phase-3"></a>
## Phase 3: Your Legal Theories — The Substance

You have **5 viable causes of action**. Here's the case law foundation for each.

### Theory 1: Breach of Contract + Duty of Honest Performance

**Landmark**: *Bhasin v. Hrynew*, 2014 SCC 71

The SCC recognized:
- A **general organizing principle of good faith** underlying contract law
- A **duty of honest performance**: parties must not lie or knowingly mislead each other about matters directly linked to contract performance
- This duty applies to **all contracts** and **cannot be contracted out of**
- It does NOT require a duty of disclosure — but you **cannot actively deceive**

**Development — *C.M. Callow Inc. v. Zollinger*, 2020 SCC 45**:
- Extended Bhasin: the duty applies to both **performance of obligations AND exercise of rights**
- While there's no positive duty to disclose, you **must correct false impressions you created**
- Even an "unfettered right to terminate" doesn't exempt you from honest performance

**Application to your case**: TON's conduct — denying plans while secretly pursuing NRG Bloom's contacts, misrepresenting intentions — maps directly to Bhasin/Callow. If TON misled NRG Bloom about the partnership while secretly circumventing, that's a textbook breach of honest performance.

**Damages**: Calculated on the basis of what NRG Bloom's economic position **would have been** had TON performed honestly (Bhasin awarded $87K on this basis).

**Key Citations**:
- *Bhasin v. Hrynew*, [2014 SCC 71](https://www.canlii.org/en/ca/scc/doc/2014/2014scc71/2014scc71.html)
- *C.M. Callow Inc. v. Zollinger*, [2020 SCC 45](https://www.canlii.org/en/ca/scc/doc/2020/2020scc45/2020scc45.html)

---

### Theory 2: Breach of Fiduciary Duty

**Foundational test**: *Frame v. Smith*, [1987] 2 SCR 99 (Wilson J.)

Three hallmarks of a fiduciary relationship:
1. **The fiduciary has scope for exercise of discretion** over the other party's interests
2. **The fiduciary can unilaterally affect** the other party's legal or practical interests
3. **The beneficiary is vulnerable** to the fiduciary's exercise of that discretion

**Refined by**: *Alberta v. Elder Advocates of Alberta Society*, 2011 SCC 24
- Not every relationship involving trust is fiduciary
- Requires evidence of a **mutual understanding** that one party has relinquished self-interest and agreed to act solely on behalf of the other

**In the JV context**: Alberta courts do **not automatically** impose fiduciary duties between joint venturers. The analysis is fact-specific:
- Did the JV structure give TON discretion over NRG Bloom's interests?
- Was NRG Bloom vulnerable to TON's exercise of that discretion?
- Was there a mutual understanding of loyalty?

**Your argument**: The Co-Management Agreement and the nature of the partnership (NRG Bloom contributed contacts and technology; TON had on-the-ground operational control) may create the vulnerability and discretion required. The power imbalance — TON controlling operations in Nigeria while NRG Bloom relied on them from Canada — fits the Frame v. Smith indicia.

**Key Citations**:
- *Frame v. Smith*, [1987 SCC](https://www.canlii.org/en/ca/scc/doc/1987/1987canlii74/1987canlii74.html)
- *Hodgkinson v. Simms*, [1994 SCC](https://www.canlii.org/en/ca/scc/doc/1994/1994canlii70/1994canlii70.html)
- *Elder Advocates*, [2011 SCC 24](https://www.canlii.org/en/ca/scc/doc/2011/2011scc24/2011scc24.html)
- Alberta Law Reform Institute, "Joint Ventures" — [Report](https://www.alri.ualberta.ca/wp-content/uploads/2020/05/FR-99_hyperlinks.pdf)

---

### Theory 3: Breach of Confidence

**Landmark**: *Lac Minerals Ltd v. International Corona Resources Ltd*, [1989] 2 SCR 574

Three elements:
1. **Confidential information** was communicated (business plans, financial models, contacts)
2. **In confidence** — the recipient knew it was confidential
3. **Misused by the recipient** to the detriment of the confider

**Critical holdings from Lac Minerals**:
- **No confidentiality agreement required**: "There was no reason to clutter normal business practice by requiring a contract. Business and accepted morality are not mutually exclusive domains."
- The recipient was **aware** it owed obligations of good faith
- But for the recipient's actions, the confider **would probably have** acquired the opportunity
- Remedy: **constructive trust** — not just damages, but return of what was taken

**Application to your case**: NRG Bloom disclosed business plans, financial models, and introduced TON to its contacts (Axxela, Nigerian partners). These were communicated in the context of a partnership (confidential by nature). TON used those introductions and that information to circumvent NRG Bloom. This maps directly to Lac Minerals.

**Key advantage**: Breach of confidence does NOT require proving a fiduciary relationship. The SCC in Lac Minerals held 5-0 on breach of confidence, while only 3-2 on fiduciary duty.

**Key Citations**:
- *Lac Minerals v. International Corona*, [1989 SCC](https://www.canlii.org/en/ca/scc/doc/1989/1989canlii34/1989canlii34.html)
- Lac Minerals Wikipedia overview for accessible summary

---

### Theory 4: Tortious Interference with Economic Relations

**Landmark**: *A.I. Enterprises Ltd. v. Bram Enterprises Ltd.*, 2014 SCC 12

Elements (SCC tightened the test):
1. Defendant **intentionally** interfered with plaintiff's economic interests
2. By **unlawful means** — conduct that would be actionable by a third party or otherwise unlawful
3. The interference caused **damage**

**The "unlawful means" requirement is strict**: After *Bram Enterprises*, you need to show the defendant used independently actionable conduct. This means the breach of contract or breach of confidence **itself** can serve as the unlawful means — but simple competitive behavior is not enough.

**Application**: If TON used confidential information (breach of confidence = unlawful means) to interfere with NRG Bloom's relationship with Axxela or other partners, this theory works. The breach of the NDA/Non-Circumvention agreement provides the unlawful means.

---

### Theory 5: Similar Fact Evidence — Phoenix Trading Prior Lawsuit

**The question**: Can Tyler MacPhearson's 2022 US lawsuit (Phoenix Trading FZCO v. Dennis Corp, 4:22-cv-02355, D.S.C.) be used as evidence of a pattern of conduct?

**In Canadian civil cases**: Similar fact evidence is treated differently than in criminal cases.

Key points:
- Civil standard is **balance of probabilities**, not beyond reasonable doubt
- Evidence of prior similar conduct is admissible if it is **relevant** to a fact in issue
- The judge weighs **probative value against prejudicial effect**
- Prior bad acts can be admitted to show: **system, pattern, plan, or modus operandi**

**Your argument**: The Phoenix Trading lawsuit alleges strikingly similar conduct — crypto mining partnerships where Tyler/defendants allegedly misappropriated the partnership and cut out the original partners. This goes to:
- **Pattern of conduct** (not an isolated incident)
- **Intent** (deliberate, not accidental)
- **Credibility** (if TON claims misunderstanding, the prior lawsuit undermines that)
- **Punitive damages threshold** (repeat conduct supports aggravated/punitive award)

**Authentication of US court documents**: US court records are public records. To admit them in Canadian proceedings, you'll need to authenticate them (likely through a certified copy from the US court). Foreign public documents can be admitted through judicial notice or as exhibits.

---

### Theory 6: Punitive and Aggravated Damages

**Landmark**: *Whiten v. Pilot Insurance Co.*, 2002 SCC 18

Punitive damages are available in Canadian commercial disputes when the defendant's conduct is:
- **Harsh, vindictive, reprehensible and malicious**
- Constitutes a **marked departure** from ordinary standards of decent behavior
- An **independent actionable wrong** exists (breach of contract alone is usually insufficient, but breach of fiduciary duty or breach of confidence qualifies)

**Your argument for punitive damages**:
1. TON's conduct was not merely negligent — it was a **deliberate scheme**
2. The Phoenix Trading prior lawsuit shows this is **repeat behavior** — heightening the reprehensibility
3. Multiple legal wrongs (breach of contract + breach of confidence + breach of fiduciary duty) compound the severity
4. The pattern suggests TON specifically targets partnerships to exploit and then discard

---

<a name="phase-4"></a>
## Phase 4: Evidence Rules — Getting Your Proof Admitted

### Governing Legislation

| Statute | Scope |
|---------|-------|
| **Canada Evidence Act** (ss. 31.1–31.8) | Federal rules for electronic documents |
| **Alberta Evidence Act** (RSA 2000, c A-18, ss. 41.1–41.8) | Provincial rules for electronic records |
| **Alberta Electronic Transactions Act** (SA 2001, c E-5.5) | Supports integrity of electronic records |

### Authentication — The Low Bar

Under **s. 31.1 CEA** and **s. 41.3 Alberta Evidence Act**:

> "A person seeking to introduce an electronic record as evidence has the burden of proving its authenticity by evidence **capable of supporting a finding** that the electronic record is **what the person claims it to be**."

This creates a **very low threshold**. You need "some evidence" — not proof beyond a doubt.

From *R. v. Martin* (NLCA 2021): "There must be evidence capable of supporting a finding that the electronic evidence sought to be admitted is what it purports to be" — a **very low threshold** for admissibility.

### Best Evidence Rule for Electronic Documents

Under **s. 31.2 CEA** and **s. 41.4 Alberta Evidence Act**, the best evidence rule is satisfied by:

1. **Proof of the integrity of the electronic records system** (WhatsApp, email server), OR
2. **Evidentiary presumption** — in the absence of evidence to the contrary, system integrity is **presumed**

**Key point**: A printout that has been "manifestly or consistently acted on, relied on, or used as the record" **IS** the record for best evidence purposes.

### Your Evidence — How to Authenticate Each Type

#### WhatsApp Messages (2,700+)

- WhatsApp exports fall within "electronic documents" under s. 31.8 CEA
- Authentication threshold is **low** — you need to testify (or swear an affidavit) that the exports are what they purport to be
- You do NOT need to identify the author at the authentication stage
- The system integrity of WhatsApp is generally presumed (end-to-end encrypted, timestamped)
- **Best practice**: Use the native WhatsApp export function (not screenshots) — this preserves metadata and is harder to challenge

**Caution from Ontario CA**: "There are entirely too many ways for an individual to make electronic evidence appear to be something other than what it is. Trial judges need to be rigorous in their evaluation."

**Your advantage**: You have **native exports**, not screenshots. This is stronger evidence.

#### Emails (84+)

- Same framework as WhatsApp — electronic documents under CEA
- Email headers contain metadata (sender, receiver, timestamp, server path)
- Authentication: testify that these are emails you sent/received in the ordinary course of business
- Gmail provides reliable system integrity (Google's infrastructure)

#### Call Transcripts (4)

- If recorded with consent of at least one party (you), admissible under Canadian law
- One-party consent is legal in Canada under s. 184(2) of the Criminal Code
- Authenticate through your testimony about when/how recorded

#### US Court Records (Phoenix Trading)

- Public records from a foreign court
- Authenticate through: certified copies from the US court clerk, or judicial notice
- PACER records include case numbers, filing dates, and court stamps
- May need to obtain certified copies — contact Dillon County Clerk of Court: (843) 774-1421

### Hearsay — The Key Exception

Your evidence is largely **not hearsay** for the most critical purpose:

- **Admissions by party opponents**: Statements by Tyler/TON are admissible **against them** as admissions — they are NOT hearsay when offered against the party who made them
- WhatsApp messages FROM Tyler = admissions by a party opponent
- This covers most of your "game-changer" evidence

For third-party statements in the chats:
- **Business records exception** (s. 30 CEA): Records made in the usual and ordinary course of business are admissible
- **Necessity + reliability**: If the declarant is unavailable, the statement can be admitted if it is necessary and reliable

### Affidavit of Records (Alberta Rules of Court)

When you commence an action, you'll need to produce an **Affidavit of Records** — a sworn list of all relevant documents in your possession. This includes:

1. **Producible documents** — documents you're willing to produce (your evidence)
2. **Privileged documents** — documents you claim privilege over (legal advice, strategy)
3. **Documents no longer in your possession** — documents you had but no longer have

**Timeline**: Under the 2025 Litigation Plan rules, disclosure of records must be completed within **10 months** of the trigger date.

### Action Items

- [ ] Organize all WhatsApp exports by chat, with date ranges
- [ ] Create a master evidence index with document ID, date, participants, and key content
- [ ] Preserve metadata — do not alter original export files
- [ ] Prepare an affidavit authenticating your electronic evidence
- [ ] Obtain certified copies of Phoenix Trading court records

---

<a name="phase-5"></a>
## Phase 5: AI in Canadian Courts — Rules of Engagement

### Current Landscape (2024-2026)

Canadian courts are actively regulating AI use. Here's what you need to know as an SRL.

### Court-by-Court AI Rules

| Court | Requirement | Since |
|-------|------------|-------|
| **Federal Court** | Declaration in first paragraph if AI generated content | May 7, 2024 |
| **Ontario SCJ** | Certification of legal authorities as authentic (O. Reg 384/24) | December 1, 2024 |
| **BC Supreme Court** | Disclose when materials include AI-generated content | March 2024 |
| **Nova Scotia** | Identify which AI tool was used and how | 2024 |
| **Alberta** | **No specific AI practice direction yet** — but general obligations of accuracy apply |
| **Trademarks Board** | Declaration required; all AI content must be verified | June 2025 |

### The Hallucination Trap

Two cautionary cases:

1. **Zhang v. Chen** (2024 BCSC 285): Lawyer cited two non-existent authorities from ChatGPT. Personally liable for costs.
2. **Hussein v. Canada** (2025 FC 1060): Lawyer submitted AI-hallucinated cases. **Special costs** imposed (reserved for "reprehensible conduct").

### Rules for You as an SRL

1. **ALWAYS verify every case citation** — look it up on CanLII before citing it
2. **Disclose AI use** if the court requires it (even if Alberta doesn't yet have a specific rule, transparency protects you)
3. **AI is a research tool, not a citation source** — use it to find leads, then verify on CanLII
4. **Draft with AI, but own every word** — you are responsible for everything in your filings
5. **Law Society rules apply to lawyers, not SRLs** — but courts expect the same standards of accuracy from everyone

### Presumptively Authentic Sources (Ontario Standard — Good Practice Everywhere)

These sources are presumed authentic without further verification:
- Government websites
- CanLII
- Commercial publishers (Lexis, Westlaw)
- Scholarly journals

### Free Legal Research Tools for SRLs

| Tool | URL | Cost |
|------|-----|------|
| **CanLII** | [canlii.org](https://www.canlii.org) | FREE — primary source for Canadian case law and legislation |
| **Alberta King's Printer** | [king's-printer.alberta.ca](https://kings-printer.alberta.ca) | FREE — Alberta statutes and regulations |
| **SOQUIJ** | [soquij.qc.ca](https://soquij.qc.ca) | FREE — Quebec case law |
| **Alberta Courts** | [albertacourts.ca](https://albertacourts.ca) | FREE — forms, practice directions, announcements |
| **LawCentral Alberta** | [lawcentralalberta.ca](https://www.lawcentralalberta.ca) | FREE — SRL guides and resources |

### Your AI Workflow (Safe Practice)

```
1. Use AI (Claude, etc.) to research legal theories and find relevant case names
2. Look up EVERY case on CanLII — verify it exists and says what AI claims
3. Read the actual decision — understand the ratio (the binding legal principle)
4. Draft your arguments referencing verified CanLII citations
5. If filing in a court with AI disclosure rules, include the declaration
6. Keep a research log: what AI tools you used, what you verified, what you discarded
```

---

<a name="phase-6"></a>
## Phase 6: Costs & Risk Management

### Alberta Costs Regime

In Canada, the general rule is **loser pays** — the unsuccessful party typically pays a portion of the successful party's legal costs. This is different from the US "American Rule" where each side pays their own.

### Costs for SRLs

- SRLs **can recover some costs** if they win — but typically less than what a represented party would receive
- If you **lose**, you may be ordered to pay TON's costs — but courts are generally moderate with SRL cost awards
- Cost awards in Alberta follow **Schedule C** of the Rules of Court — a tariff-based system, not actual costs

### Mitigating Your Risk

1. **Settlement offers (Calderbank letters)**: Making a formal settlement offer can protect you on costs — if you beat your own offer at trial, the other side pays enhanced costs
2. **Fee waiver**: If finances are tight, apply for a court fee waiver
3. **Cost cap**: Some courts will set a costs cap in advance for SRL proceedings
4. **The real risk calculation**: What's your downside exposure vs. the value of your claim? If damages are $1.6M+ and cost exposure is $20-50K, the ratio favors proceeding

---

<a name="phase-7"></a>
## Phase 7: Service on International Parties

### Serving TON Infrastructure Ltd. (Nigerian-Connected Entity)

This is one of the most complex procedural challenges you'll face.

### Key Questions

1. **Is TON incorporated in Nigeria, Alberta, or elsewhere?** This determines which service rules apply.
2. **Does TON have a registered agent or office in Alberta/Canada?** If yes, serve through the registered agent.
3. **Does the contract specify a service address?** Check all 4 agreements.

### Alberta Rules for International Service

- **Hague Convention**: Nigeria is NOT a party to the Hague Service Convention — so simplified Hague procedures don't apply
- **Alternative service**: You can apply to the court for an order allowing service by alternative means (email, registered mail, etc.)
- **Service ex juris** (outside jurisdiction): Alberta Rules of Court permit service outside Alberta in certain circumstances, including breach of contract claims where the contract was made or was to be performed in Alberta

### Practical Approach

1. Check if TON has any Canadian presence (office, agent, director with Canadian address)
2. If yes, serve through that Canadian presence
3. If no, apply to the court for an order for **substitutional service** (service by email to known email addresses, for example)
4. Tyler MacPhearson likely has a Canadian connection (the agreements were made with a Canadian company) — research his current address

---

<a name="phase-8"></a>
## Phase 8: Tools & Resources for SRLs

### Alberta-Specific Resources

| Resource | What It Provides | URL |
|----------|-----------------|-----|
| **LawCentral Alberta** | SRL guides, court forms, step-by-step instructions | [lawcentralalberta.ca](https://www.lawcentralalberta.ca) |
| **Court Forms Information Coordinators** | Help with locating and filling out forms | At any Alberta courthouse |
| **Alberta Law Libraries** | Free access to legal databases, research assistance | [lawlibrary.ab.ca](https://lawlibrary.ab.ca) |
| **Pro Bono Law Alberta** | Free legal advice clinics | [pbla.ca](https://pbla.ca) |
| **Legal Aid Alberta** | May provide duty counsel advice (income-tested) | [legalaid.ab.ca](https://legalaid.ab.ca) |
| **Resolution & Court Admin Services (RCAS)** | ADR services, mediation | Through the court |

### National Resources

| Resource | What It Provides |
|----------|-----------------|
| **National Self-Represented Litigants Project (NSRLP)** | Research, guides, advocacy for SRLs |
| **CLEO (Community Legal Education Ontario)** | Legal information guides (some applicable nationally) |
| **CanLII** | Free case law and legislation database |
| **Steps to Justice** | Plain-language legal guides |

### Key Court Links

- Alberta Courts homepage: [albertacourts.ca](https://albertacourts.ca)
- King's Bench civil forms: [albertacourts.ca/kb/areas-of-law/civil/forms](https://www.albertacourts.ca/kb/areas-of-law/civil/forms)
- Court fees: [alberta.ca/court-fees](https://www.alberta.ca/court-fees)
- Alberta Rules of Court: [CanLII](https://www.canlii.org/en/ab/laws/regu/alta-reg-124-2010/)
- Alberta Limitations Act: [CanLII](https://www.canlii.org/en/ab/laws/stat/rsa-2000-c-l-12/)
- Alberta Evidence Act: [CanLII](https://www.canlii.org/en/ab/laws/stat/rsa-2000-c-a-18/latest/rsa-2000-c-a-18.html)
- Alberta Arbitration Act: [CanLII](https://www.canlii.org/t/822r)

---

<a name="study-sequence"></a>
## Study Sequence — What to Learn First

### Priority Order (Time-Sensitivity Drives the Sequence)

| Order | Topic | Why First | Time Required |
|-------|-------|-----------|--------------|
| **1** | Limitation period analysis | If your clock is running, nothing else matters until you file | 1-2 days |
| **2** | Protective filing mechanics | How to actually file a Statement of Claim in Alberta | 1 day |
| **3** | Forum selection (arbitration vs. court) | Determines your entire strategy | 2-3 days |
| **4** | Legal theories deep-dive | Understand your causes of action inside-out | 1 week |
| **5** | Evidence organization | Prepare your Affidavit of Records | 1 week |
| **6** | Service rules | How to serve TON (international complexity) | 2-3 days |
| **7** | AI tools and verification workflow | Set up your research process | Ongoing |
| **8** | Costs and risk assessment | Know your downside before committing | 1 day |

### Recommended Study Method

For each topic:
1. **Read the statute** on CanLII (the actual law, not summaries)
2. **Read 2-3 leading cases** (the ones cited in this roadmap)
3. **Look for Alberta-specific applications** (Alberta Court of King's Bench and Alberta Court of Appeal decisions)
4. **Draft your position** on each issue as if you're writing it for a judge
5. **Pressure-test with AI** — ask Claude to challenge your position and find weaknesses

### Living Document Tracking

| Topic | Status | Last Studied | Key Gaps |
|-------|--------|-------------|----------|
| Limitation period | Not started | — | Need to calculate discovery date |
| Filing mechanics | Not started | — | Need to confirm current fees |
| Forum selection | Not started | — | Need to analyze Section 7 scope |
| Bhasin/honest performance | Familiar | — | Need to read Callow deeply |
| Fiduciary duty | Familiar | — | Need Frame v. Smith test details |
| Breach of confidence | Familiar | — | Lac Minerals — strong fit |
| Tortious interference | Familiar | — | Bram Enterprises unlawful means req |
| Evidence rules | Not started | — | WhatsApp authentication specifics |
| AI disclosure rules | Not started | — | Alberta-specific guidance |
| Costs regime | Not started | — | Schedule C tariff research |
| International service | Not started | — | Nigeria-specific challenges |

---

## Key Case Law Quick Reference

| Case | Year | Court | Principle |
|------|------|-------|-----------|
| *Bhasin v. Hrynew* | 2014 | SCC | Duty of honest performance in all contracts |
| *C.M. Callow v. Zollinger* | 2020 | SCC | Must correct false impressions; duty can't be contracted out |
| *Frame v. Smith* | 1987 | SCC | Three indicia of fiduciary relationships |
| *Elder Advocates v. Alberta* | 2011 | SCC | Not every relationship of trust is fiduciary |
| *Hodgkinson v. Simms* | 1994 | SCC | Ad hoc fiduciary duties in advisory relationships |
| *Lac Minerals v. Corona* | 1989 | SCC | Breach of confidence — no contract needed |
| *A.I. Enterprises v. Bram* | 2014 | SCC | Tortious interference requires "unlawful means" |
| *Whiten v. Pilot Insurance* | 2002 | SCC | Punitive damages threshold |
| *Peace River v. Petrowest* | 2022 | SCC | Mandatory stay for arbitration — narrow exceptions |
| *Husky Oil v. Technip* | 2024 | ABCA | Arbitration clause doesn't bind third parties without clear language |
| *Agrium v. Orbis* | 2022 | ABCA | Delay/participation can waive right to arbitrate |
| *Grant Thornton v. New Brunswick* | 2021 | SCC | "Plausible inference" starts limitation clock |
| *Zhang v. Chen* | 2024 | BCSC | AI hallucinated citations — lawyer personally liable for costs |

---

## Disclaimer

This roadmap is a **research and study guide**, not legal advice. All case citations should be verified on CanLII before reliance. The information reflects research current as of March 2026 and may not capture all recent developments. For critical decisions (especially limitation periods and protective filings), consider consulting with a lawyer even briefly — many offer free initial consultations, and Alberta has pro bono resources for self-represented litigants.

---

*This roadmap was built using AI-assisted research across 15+ web searches covering Alberta civil procedure, arbitration law, evidence rules, legal theories, and access to justice resources. All case citations are drawn from search results referencing CanLII, SCC decisions, and Alberta Court of Appeal decisions.*
