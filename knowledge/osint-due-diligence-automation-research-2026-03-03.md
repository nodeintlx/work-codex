# OSINT & Due Diligence Automation — Research Report
# Saved from research agent output — March 3, 2026
# Full report captured from agent ab58ba3aae83ec68f

See full agent output at: /private/tmp/claude-502/-Users-xbtsupernode-Work/tasks/ab58ba3aae83ec68f.output

## Key Findings Summary

### OSINT Tools — Agent-Ready Assessment
- **SpiderFoot OSS** (free): Best automation backbone. REST API, 200+ sources. Use this.
- **Social Links SL API** ($0.15-$0.40/call): Best paid per-call OSINT. Social/blockchain/dark web
- **Maltego** ($6,600/yr): GUI-driven, not agent-friendly. Human analyst tool only
- **Shodan** ($49 one-time or $69/mo): Excellent API, infrastructure/exposure checks
- **theHarvester** (free): Email/subdomain harvesting. CLI, simple
- **Recorded Future / Flashpoint / Babel Street / Palantir**: All enterprise-tier, inaccessible

### Corporate Registry APIs
- **SEC EDGAR**: Free, no auth, full REST API — US public companies
- **Companies House UK**: Free, full REST API — UK companies + beneficial ownership
- **GLEIF**: Free, no auth — LEI lookup + corporate hierarchy (underused gem)
- **Zefix**: Free REST API — Swiss commercial register
- **OpenCorporates**: GBP 2,250/yr commercial — 200+ jurisdictions, single normalized API
- **D&B, Orbis, Capital IQ**: All enterprise $50K+ — inaccessible at small scale

### Sanctions & PEP Screening
- **OpenSanctions** (self-hosted, Docker): Free non-commercial. 269+ datasets. PEP limited to 28 countries
- **ComplyAdvantage Starter**: $99.99/mo — commercial-grade PEP + sanctions + adverse media API
- **sanctions.io**: 75+ lists, 1M+ PEPs, sub-350ms API. Good alternative
- **OFAC SLS**: Free bulk download
- **World-Check / Dow Jones**: Enterprise only, inaccessible

### Court Records
- **CourtListener RECAP** (free): US federal litigation, REST API, millions of documents
- **CanLII** (free): Canadian case law, all provinces. No API
- **BAILII** (free): UK/Irish case law. No API
- **PACER**: $0.10/page, usually free (<$30/quarter)

### Adverse Media
- **GDELT DOC API** (free): Global news, 65 languages. ~55% accuracy — signal detection only
- **Web search + LLM synthesis**: Effective with human review layer
- **ComplyAdvantage**: NLP-classified adverse media, 10M+ pages/day, 200+ countries

### DD Report Structure (Industry Standard)
1. Executive Summary + risk rating
2. Subject Identification
3. Corporate Affiliations
4. Sanctions/Watchlist Screening
5. PEP/Regulatory Status
6. Litigation History
7. Adverse Media
8. Financial Intelligence
9. Source Disclosure
10. Appendices

### Cost for Production MVP Stack
- Free tier: ~$0/month (EDGAR, Companies House, GLEIF, CourtListener, OpenSanctions, GDELT)
- Production tier: ~$350-$500 CAD/month (OpenCorporates + ComplyAdvantage + Shodan)

### Market Position
- Kroll/FTI: $3,000-$15,000+ per DD report, 5-10 business days
- Coldstorm AI-assisted: $500-$1,500 per report, 24-48 hour turnaround
- Position: "AI-accelerated, human-verified" — NOT "fully automated"

### Liability Rules
- Every adverse finding must have source URL
- AI claims must be human-verified before delivery
- Include methodology disclaimer
- Get E&O insurance before commercial delivery
