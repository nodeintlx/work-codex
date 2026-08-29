# Coldstorm SEO Action Plan

*Prepared: April 7, 2026*

## Goal

Make `coldstorm.org` easier to:

- find in search
- crawl and understand
- trust quickly
- contact when someone has an urgent investigation, litigation, or compliance need

This plan is based on the live site structure and the generated site snapshot in `/home/dowsmasternode/tmp/coldstorm-ga-pass/site`.

## What Is Working

- The site already has crawlable HTML pages, canonical tags, sitemap coverage, and reasonable meta descriptions.
- The blog has useful long-tail content and several pages already use `Article`, `FAQPage`, and `BreadcrumbList` schema.
- Core service areas exist as dedicated URLs rather than hidden inside a single homepage.

## Main Problems

1. The site does not yet have a clean indexable hub structure for services and authority pages.
2. Several litigation-intelligence pages overlap too closely and will compete with each other.
3. The strongest trust and availability signals are present, but not consistently emphasized across the site.
4. Case studies are bundled into one page instead of separate rankable proof pages.
5. Internal links are good, but not yet organized around a deliberate topic-cluster model.

## Sitewide Changes

### 1. Add a real `/services/` hub page

Create a dedicated `https://coldstorm.org/services/` page.

Why:

- Blog and service breadcrumbs currently point "Services" to `/#services`, which is not a strong crawl target.
- A real hub gives search engines a clean parent page for all commercial offerings.
- It gives visitors a fast way to understand what you do and that you are available now.

This page should:

- list all services with short summaries
- state who each service is for
- include response-time language such as "urgent tracing intake available"
- link to `Contact` and `Urgent Intake`
- link to key case studies

Pages that should switch their breadcrumb and nav references from `/#services` to `/services/`:

- [blockchain-forensics service](/home/dowsmasternode/tmp/coldstorm-ga-pass/site/services/blockchain-forensics/index.html#L57)
- [litigation-intelligence page](/home/dowsmasternode/tmp/coldstorm-ga-pass/site/litigation-intelligence/index.html#L125)
- most blog posts that currently reference `/#services`

### 2. Add an `/about/` or `/about/makir-volcy/` authority page

Right now the site shows strong credibility signals, but they are distributed across pages and schema. Make them explicit in one crawlable page.

Include:

- Makir Volcy bio
- former roles and investigation/compliance experience
- Chainalysis / surveillance / trading background
- languages served
- geography served
- what types of matters are a fit
- direct contact details
- "currently accepting new engagements" language

This page supports E-E-A-T and improves conversion by making the operator behind the site legible.

### 3. Split case studies into separate URLs

Keep `/case-studies/` as the hub, but add individual pages:

- `/case-studies/blockchain-forensics-urgent-tracing/`
- `/case-studies/litigation-intelligence-commercial-dispute/`
- `/case-studies/crypto-compliance-program-design/`

Each page should include:

- situation
- evidence landscape
- what Coldstorm did
- result
- constraints
- deliverable format
- who the engagement was for
- CTA to contact or schedule a scoping call

These pages will rank for high-trust long-tail queries and make the commercial pages more believable.

### 4. Standardize brand and trust signals

Use one naming format across titles and metadata:

- prefer `Coldstorm AI`

Also add the same trust block to every service page:

- availability status
- direct email
- phone
- expected response time
- geography served
- "work with law firms, victims, exchanges, fintechs, and compliance teams"

## Page-by-Page Actions

## Homepage

Target URL:

- `https://coldstorm.org/`

Primary job:

- brand page
- commercial overview
- routing page to the right service

Keep:

- yes

Changes:

- tighten the homepage keyword focus around the three main commercial buckets:
  - blockchain forensics
  - litigation intelligence
  - crypto compliance
- add a short "Who this is for" section near the top
- add a short "Available now for" section near the CTA
- add links to the new `/services/` hub and `/about/` page
- add 3 direct text links under the hero:
  - `Urgent crypto tracing`
  - `Commercial dispute evidence analysis`
  - `Crypto compliance advisory`

Reason:

The homepage is currently strong, but it should route humans and crawlers more clearly to the right intent path.

## Services Hub

Target URL:

- `https://coldstorm.org/services/`

Primary job:

- top-level commercial hub

Action:

- create this page

Suggested sections:

- what Coldstorm does
- service cards
- when to contact us
- proof and case studies
- FAQs
- urgent intake CTA

## Blockchain Forensics Service

Target URL:

- `https://coldstorm.org/services/blockchain-forensics/`

Primary keyword set:

- blockchain forensics
- crypto investigations
- stolen crypto tracing
- blockchain tracing consultant

Keep:

- yes

Changes:

- strengthen the first 100 words around emergency use cases and evidence-ready output
- add a visible "response time" promise if operationally true
- add FAQ blocks for:
  - how quickly tracing can start
  - whether lawyers can use the report
  - what chains and evidence types are supported
- add internal links to:
  - `/contact/urgent-tracing/`
  - relevant case study
  - `What To Do In The First 24 Hours After Your Crypto Is Stolen`
  - `When A Lawyer Should Bring In A Blockchain Forensics Specialist`

Reason:

This is likely one of the highest-conversion pages on the site. It should be more obviously urgent and more obviously available.

## Crypto Compliance Service

Target URL:

- `https://coldstorm.org/services/crypto-compliance/`

Primary keyword set:

- crypto compliance consultant
- FINTRAC crypto compliance
- market surveillance consulting
- AML investigations consultant

Keep:

- yes

Changes:

- make the page more explicit about who hires you:
  - exchanges
  - brokers
  - fintechs
  - startup operators
- link directly to the FINTRAC article and the market surveillance article
- add a section titled `When to Bring in Coldstorm`
- add a short engagement model section:
  - one-off review
  - remediation sprint
  - ongoing advisory

Reason:

This page should rank on buyer-intent compliance searches, not just describe capabilities.

## Fractional CCO Service

Target URL:

- `https://coldstorm.org/services/fractional-cco/`

Primary keyword set:

- fractional CCO crypto
- interim chief compliance officer crypto
- compliance leadership for exchanges

Keep:

- yes

Changes:

- make this page more founder/operator-facing
- explain stage-fit:
  - pre-launch
  - preparing for registration
  - post-incident remediation
- add a comparison block:
  - full-time CCO vs fractional CCO
- add explicit availability and engagement scope

Reason:

This is a valuable service, but the search volume is lower and trust threshold is higher. The page needs clearer decision-stage framing.

## AI Solutions Service

Target URL:

- `https://coldstorm.org/services/ai-solutions/`

Primary keyword set:

- compliance automation consultant
- AI agent development for compliance
- custom AI systems for investigations

Keep:

- yes

Changes:

- narrow positioning so it does not read like a generic AI agency page
- frame it as systems for:
  - compliance operations
  - investigations
  - evidence workflows
- link to the five-system proof where appropriate
- include two or three concrete implementation examples

Reason:

Generic AI services pages are hard to rank. This page should inherit authority from your investigation and compliance expertise.

## Litigation Intelligence Page

Target URL:

- `https://coldstorm.org/litigation-intelligence/`

Primary keyword set:

- litigation intelligence
- AI evidence analysis
- multi-channel evidence analysis
- litigation AI consultant

Keep:

- yes, as the main commercial page for the litigation cluster

Changes:

- make this the single primary money page for litigation-intelligence leads
- add a "Best fit matters" section:
  - commercial disputes
  - arbitration
  - founder disputes
  - evidence spread across multiple channels
- add clearer contact language:
  - scoping call
  - response window
  - what to send before the first call
- add proof links to case studies
- add a visible "not a generic legal AI platform" comparison block

Reason:

This page should be the destination page that supporting articles feed.

## Contact Page

Target URL:

- `https://coldstorm.org/contact/`

Keep:

- yes

Changes:

- add "currently accepting new engagements" language near the top
- add matter-type routing:
  - urgent tracing
  - dispute evidence analysis
  - compliance advisory
  - fractional CCO
- add expected reply timing
- add a "what to include in your inquiry" section

Reason:

This page is conversion-critical. It should reduce uncertainty and make you feel reachable.

## Urgent Tracing Intake

Target URL:

- `https://coldstorm.org/contact/urgent-tracing/`

Keep:

- yes

Changes:

- link to it more aggressively from homepage, blockchain-forensics page, and relevant blog posts
- add trust copy around confidentiality, evidentiary handling, and immediate next steps
- add a plain-language checklist:
  - wallet addresses
  - transaction hashes
  - exchange screenshots
  - timeline of events

Reason:

This is likely your best page for high-intent urgent searchers. It should be easier to reach from everywhere.

## Blog Hub

Target URL:

- `https://coldstorm.org/blog/`

Keep:

- yes

Changes:

- group articles by topic cluster instead of a flat feed:
  - blockchain forensics
  - litigation intelligence
  - crypto compliance
- feature one primary article per cluster
- add "Start here" links to the core service pages

Reason:

The blog should help search engines understand topic ownership, not just list recent posts.

## Blog Actions: Keep, Merge, Reposition

### Keep as informational cluster leaders

- `https://coldstorm.org/blog/what-is-litigation-ai/`
- `https://coldstorm.org/blog/multi-channel-evidence-analysis/`
- `https://coldstorm.org/blog/ai-contradiction-detection/`
- `https://coldstorm.org/blog/first-24-hours-after-crypto-theft/`
- `https://coldstorm.org/blog/when-lawyer-should-bring-in-blockchain-forensics-specialist/`
- `https://coldstorm.org/blog/fintrac-compliance-2026/`
- `https://coldstorm.org/blog/market-surveillance-crypto/`
- `https://coldstorm.org/blog/ai-aml-investigations/`

These are good support pages for the main services.

### Reposition, consolidate, or de-duplicate

- `https://coldstorm.org/blog/ai-evidence-analysis-service/`
- `https://coldstorm.org/blog/multi-channel-evidence-analysis-service/`
- `https://coldstorm.org/blog/general-vs-litigation-ai/`
- `https://coldstorm.org/blog/ai-vs-junior-lawyers/`
- `https://coldstorm.org/blog/deploy-vs-hold-evidence-strategy/`

Recommended treatment:

- keep `ai-vs-junior-lawyers` as awareness content
- keep `general-vs-litigation-ai` as comparison content
- keep `deploy-vs-hold-evidence-strategy` as strategic support content
- merge or strongly differentiate `ai-evidence-analysis-service` and `multi-channel-evidence-analysis-service`

Best option:

- make `/litigation-intelligence/` the main commercial page
- keep `/blog/multi-channel-evidence-analysis/` as the main informational explainer
- redirect or canonicalize one of these service-like blog posts:
  - `/blog/ai-evidence-analysis-service/`
  - `/blog/multi-channel-evidence-analysis-service/`

If both remain live, they need clearly different intents:

- one page = category explainer
- one page = pricing/process page

Right now the overlap is too high.

## Internal Link Architecture

Build three explicit topic clusters.

### Cluster 1: Blockchain Forensics

Money page:

- `/services/blockchain-forensics/`

Support pages:

- `/contact/urgent-tracing/`
- `/blog/first-24-hours-after-crypto-theft/`
- `/blog/when-lawyer-should-bring-in-blockchain-forensics-specialist/`
- future case study on urgent tracing

### Cluster 2: Litigation Intelligence

Money page:

- `/litigation-intelligence/`

Support pages:

- `/blog/what-is-litigation-ai/`
- `/blog/multi-channel-evidence-analysis/`
- `/blog/ai-contradiction-detection/`
- `/blog/deploy-vs-hold-evidence-strategy/`
- `/blog/general-vs-litigation-ai/`
- `/blog/ai-vs-junior-lawyers/`
- future litigation case study pages

### Cluster 3: Crypto Compliance

Money pages:

- `/services/crypto-compliance/`
- `/services/fractional-cco/`

Support pages:

- `/blog/fintrac-compliance-2026/`
- `/blog/market-surveillance-crypto/`
- `/blog/ai-aml-investigations/`
- future compliance case study pages

Internal linking rules:

- every blog post links to exactly one primary money page near the top and again near the end
- every money page links to 2 to 4 support articles
- every case study links back to the relevant money page
- the homepage links to all cluster leaders
- the blog hub links to one featured page per cluster

## Schema and Crawl Improvements

### Add consistent schema to every commercial page

Every service page should include:

- `Service`
- `BreadcrumbList`
- `FAQPage` when FAQs are visible on the page

Every article should include:

- `Article` or `BlogPosting`
- `BreadcrumbList`
- `FAQPage` when applicable
- visible author and updated date

### Add author consistency

Use a visible author block on all blog posts:

- `By Makir Volcy`
- short credential line
- link to `/about/` or author page
- date published
- date updated

### Keep sitemap fresh

The sitemap is structurally fine. Keep it current and make sure new pages go in immediately:

- `/services/`
- `/about/`
- each case study page

## Availability and Conversion Improvements

To make people feel you are available, add the same reassuring signals across commercial pages.

Use language like:

- `Currently accepting new engagements`
- `Urgent tracing intake available`
- `Response within 1 business day`
- `For urgent matters, include wallet addresses and transaction hashes`
- `Confidential inquiry`

Add these in visible HTML, not only schema.

## Content To Add Next

Highest-value new pages:

1. `/services/`
2. `/about/`
3. `/case-studies/blockchain-forensics-urgent-tracing/`
4. `/case-studies/litigation-intelligence-commercial-dispute/`
5. `/case-studies/crypto-compliance-program-design/`
6. blog post on opposing document analysis
7. blog post on damages quantification

## 30-Day Execution Order

### Week 1

- create `/services/`
- create `/about/`
- update all breadcrumbs from `/#services` to `/services/`
- standardize titles to `Coldstorm AI`

### Week 2

- choose one primary litigation-intelligence money page
- merge or canonicalize overlapping service-like blog posts
- add visible author blocks and update dates to all blog posts

### Week 3

- split case studies into separate URLs
- add internal links from each case study to the correct service page
- add stronger contact and availability copy across all service pages

### Week 4

- publish the next two support articles
- review Search Console for indexed pages, impressions, and click-through
- improve titles and intros on pages that get impressions but low clicks

## Success Metrics

Track these monthly:

- indexed pages
- impressions by URL
- clicks by URL
- average position for primary service pages
- branded searches for `Coldstorm AI`
- contact inquiries by source page
- urgent intake submissions

## Immediate Recommendation

If only three things happen this month, do these first:

1. Create `/services/` and fix all `/#services` references.
2. Make `/litigation-intelligence/` the single primary commercial page for that cluster.
3. Publish separate case-study URLs with strong proof and direct contact CTAs.
