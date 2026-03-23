# TON Content Risk Framework

Purpose: classify photos, videos, edits, social assets, reels, drone footage, and related creative work connected to TON so they can be used in a way that strengthens the case instead of undermining it.

This is a litigation-operations tool, not final legal clearance. If an asset is not clearly safe, treat it as `hold` or `needs_lawyer_review`.

## Operating Rule

Default rule: no public posting of TON-related content during active proceedings unless the asset has been reviewed against this framework and either:

- classified as `safe_public_generic`, or
- specifically cleared by Dayo

Everything else stays private and is used for evidence, damages support, authorship proof, and settlement leverage.

## Decision Lanes

Sentinel's review sharpened the framework into four operating lanes:

### `hold`

Do not publish. Preserve for evidence, damages support, authorship proof, and later strategic use.

This is the default lane for TON-related 2025 content.

### `reserve_for_counsel`

Share only with Dayo or future counsel. Never public.

Use when the content would be strong evidence of TON's conduct, circumvention, or appropriation, or when the asset could plausibly become a hearing or filing exhibit.

### `redact_and_repurpose`

Strip all TON identifiers, site specifics, confidential information, and dispute cues, then reuse only as generic founder/portfolio content.

### `publish`

Safe to post as-is because it has no TON connection, no site-identifying features, no confidential information, and no dispute relevance.

### Label Mapping

For the inventory and earlier working docs, use this mapping:

- `safe_internal` -> `hold`
- `safe_public_generic` -> `redact_and_repurpose` or `publish`, depending on how much editing is required
- `needs_lawyer_review` -> `reserve_for_counsel`
- `do_not_publish` -> `hold` or `reserve_for_counsel`, depending on whether counsel should actively use it

## Hard Blocks

These are absolute do-not-publish categories during active proceedings unless Dayo gives explicit clearance:

1. Anything identifying the Ogboinbiri site, community, local contacts, or access path
2. TON-branded or TON-identifiable content, including names, logos, serials, or clearly traceable equipment
3. Financial data, pricing, revenue, cost structures, expenditure details, or models
4. Negotiation, mediation, without-prejudice, or settlement materials
5. Dispute communications, including emails, WhatsApp, call transcripts, and legal letters
6. Content implying current affiliation with TON
7. Accusatory or retaliatory framing aimed at TON or its people

## Risk Labels

### `safe_internal`

Use internally only:

- counsel packages
- evidence binders
- damages proof
- authorship/origination proof
- timeline reconstruction

This is now functionally equivalent to `hold`.

### `safe_public_generic`

Can potentially be used publicly without naming TON or the dispute, if all of the following are true:

- no TON name, logo, or branding
- no site-identifying features that clearly tie the asset to TON
- no confidential commercial information
- no negotiation, mediation, or dispute material
- no current-affiliation implication
- no accusation or commentary about wrongdoing

Example:
- generic founder-story footage about work in Nigeria
- neutral infrastructure visuals with identifiers removed
- creator portfolio samples stripped of client attribution

This is now functionally equivalent to `redact_and_repurpose` unless the asset is already fully generic.

### `needs_lawyer_review`

Do not publish until reviewed by counsel. Use when any of the following appear:

- TON branding or obvious TON association
- identifiable site visuals
- business terms, pricing, wallet, revenue, equipment counts, or strategy
- Axxela or third-party commercial information
- anything that could be characterized as confidential information
- anything that could look like reputational pressure during active proceedings
- anything that might imply endorsement, partnership, or current authority

This is now functionally equivalent to `reserve_for_counsel`.

### `do_not_publish`

No public use while proceedings are active. Preserve only for litigation use.

This includes:

- mediation or without-prejudice material
- demand letters, replies, settlement exchanges
- screenshots of legal correspondence
- accusations that could trigger defamation arguments
- content revealing site security, electrical layout, operations, access points, or sensitive infrastructure
- private messages or call-derived content
- content whose ownership is materially disputed

This is still the strongest no-public-use marker, but operationally it should usually live in `hold` or `reserve_for_counsel`.

## Decision Questions

For each asset, answer these in order:

1. Did Makir or NRG Bloom create this asset?
2. Is there any signed assignment or clear licence giving TON ownership or unrestricted use?
3. Does the asset show TON branding, personnel, equipment, or identifiable site features?
4. Does it reveal confidential business information, site intelligence, pricing, or third-party information?
5. Does it mention or derive from the dispute, mediation, negotiation, or legal correspondence?
6. Could public posting let TON argue breach of confidence, prejudice to proceedings, defamation, or false association?
7. Can the asset be safely edited into a generic, non-identifying version?

If the answer to 3 through 6 is "yes", do not post it. Move it into `hold` or `reserve_for_counsel`.

## Recommended Immediate Workflow

1. Inventory every asset first.
2. Mark `creator`, `date_created`, `raw_location`, and `known_use_by_ton`.
3. Start every uncategorized asset as `hold`.
4. Move only clearly generic assets to `redact_and_repurpose` or `publish`.
5. Move anything sensitive or uncertain to `reserve_for_counsel`.
6. Move mediation/dispute/confidential content to `hold` or `reserve_for_counsel`.
7. Ask Dayo to clear categories, not one-off ad hoc posts.

## What This Framework Protects Against

- breach of confidence arguments
- confidentiality arguments under the MNDA track
- mediation / without-prejudice misuse
- defamation or disparagement framing
- accidental admission that TON had marketing rights
- weakening the optics of NRG Bloom's restraint during proceedings

## What This Framework Preserves

- proof that Makir created real value
- proof that NRG Bloom built and documented the site opportunity
- a future public narrative if counsel later decides timing is right
- leverage against TON's continued use of creator-produced content

## Practical Guidance

Best current use of the content:

- evidence of origination and operational work
- proof of marketing value created by NRG Bloom
- support for unjust enrichment / appropriation narrative
- support for a future takedown / misuse complaint if TON is exploiting creator-made media

Best current public lane:

- generic founder-story content where no reader could identify TON, the site, or the dispute
- repurposed portfolio content with all TON/site identifiers removed

Worst current use of the content:

- angry public posting tied to the dispute
- naming TON while proceedings are active
- posting confidential visuals or site details
- posting anything that quotes or references settlement, mediation, or legal letters

## Initial Presumptions For This Matter

Based on current workspace evidence, use these presumptions until counsel says otherwise:

- TON-related site footage: `reserve_for_counsel`
- drone footage of the site: `reserve_for_counsel`
- edited marketing materials created for TON: `reserve_for_counsel`
- legal/dispute screenshots: `hold`
- demand/settlement correspondence: `hold`
- generic founder-story clips with all client/site identifiers removed: `redact_and_repurpose`
- raw creation files proving Makir made the assets: `hold`

## Approval Standard

Public use should be approved only if the asset is:

- creator-controlled
- non-confidential
- non-prejudicial to proceedings
- non-identifying as to TON unless counsel approves that specific use
- strategically useful rather than emotionally satisfying

## Live Rules

Effective immediately:

- default = `hold`
- if in doubt, ask Dayo before publishing
- content held back is not wasted; it is being deployed strategically as evidence
