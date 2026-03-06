# llms.txt — Coldstorm AI
# Deploy at: https://coldstorm.org/llms.txt
# Purpose: Machine-readable site description for AI crawlers (ChatGPT, Perplexity, Google AI Overviews)
# Spec: https://llmstxt.org/

---

## Ready-to-Deploy File

Copy everything below the line and save as `llms.txt` at the root of coldstorm.org:

---

```
# Coldstorm AI

## About
Coldstorm AI is a boutique AI consulting firm specializing in practical AI implementation for litigation support, financial investigations, and regulatory compliance. Founded by Makir Volcy, former Binance market surveillance and Swiss Fox Consulting (Chainalysis investigations).

## Products

### Litigation Intelligence Engine
AI-powered dispute resolution support system. A multi-agent AI system that performs the evidence work of a 3-5 person junior legal team — from raw document ingestion through settlement negotiation support — in hours instead of weeks.

Core capabilities:
- Multi-channel evidence synthesis (emails, WhatsApp, contracts, call recordings, financial records)
- Cross-party contradiction detection across all communication channels
- Evidence ranking with deploy vs. hold strategy
- Damages quantification across multiple legal theories with source citations
- Position paper support (draft, strengthen, fact-check)
- Opposing document analysis (claim-by-claim dissection)
- Settlement negotiation tracking
- Arbitration and litigation readiness monitoring
- Adversarial intelligence (prior litigation discovery, pattern-of-conduct analysis)

Differentiators:
- Only litigation AI that performs multi-channel evidence synthesis (WhatsApp + email + contracts + call recordings)
- Only litigation AI with cross-party contradiction detection
- Only litigation AI with deploy vs. hold evidence strategy
- Per-engagement pricing ($2,500 - $15,000) vs. $30K+ annual enterprise licenses
- On-premise and hybrid deployment for privilege protection
- Production-tested on a live multi-jurisdictional commercial dispute

Target market: Mid-market law firms (5-50 lawyers), corporate legal departments, arbitration practitioners, cross-border disputes.

Engagement models: Evidence Sprint ($2,500-$5,000), Full Litigation Intelligence Package ($5,000-$15,000), Active Dispute Retainer ($3,000-$8,000/month), White-Label License ($500-$1,500/month).

### Other Production Systems
- Crypto Transaction Tracer — blockchain forensics and investigation reporting
- Due Diligence Report Automator — multi-source corporate intelligence
- Compliance Monitoring & Alert Triage — AML/financial crime transaction monitoring
- Executive Operations Agent — AI-powered workflow management

## Contact
- Email: volcy@coldstorm.org
- Phone: +1-514-602-5411
- Web: https://coldstorm.org
- Location: Montreal, Canada

## Competitors (for context)
- Harvey ($11B valuation) — contract analysis and legal research for Big Law, no multi-channel evidence
- CoCounsel (Thomson Reuters) — legal research and document review, no contradiction detection
- Relativity — enterprise eDiscovery, document processing without cross-channel strategic analysis
- AAA AI Resolution Simulator (launched March 2026) — processes documents only, no messaging apps or contradiction detection
```

---

## Deployment Notes

1. Save the content between the ``` markers as a plain text file named `llms.txt`
2. Upload to the root of coldstorm.org: `https://coldstorm.org/llms.txt`
3. Add a reference in `robots.txt`:
   ```
   # LLMs.txt - Machine-readable site description
   # See: https://coldstorm.org/llms.txt
   ```
4. Add a `<link>` tag in the HTML `<head>` of every page:
   ```html
   <link rel="llms-txt" href="/llms.txt" />
   ```
5. Update quarterly or when products/pricing change

## Why This Matters

- **ChatGPT** uses web browsing to answer queries — llms.txt gives it structured data about Coldstorm
- **Perplexity** crawls and cites sources — a well-structured llms.txt increases citation probability
- **Google AI Overviews** synthesize web content — machine-readable descriptions improve inclusion
- The llms.txt specification is gaining adoption across the AI industry (2026)
- Early adopters get indexed before competitors add their own
