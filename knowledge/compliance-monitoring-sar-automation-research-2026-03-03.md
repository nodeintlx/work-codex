# Compliance Monitoring, SAR/STR Automation & KYC Intelligence — Research Report
# Saved from research agent output — March 3, 2026
# Full report captured from agent abc69f7f14b471d85

See full agent output at: /private/tmp/claude-502/-Users-xbtsupernode-Work/tasks/abc69f7f14b471d85.output

## Key Findings Summary

### Transaction Monitoring Platforms
- **Chainalysis KYT**: Cloud-only, $100K-$500K+/year. Not buildable — position as integrator
- **TRM Labs BLOCKINT API**: Most developer-accessible crypto intel API. Best for agent integration
- **Elliptic Lens**: Strong cross-chain tracing. Cloud-only, enterprise pricing
- **Eventus Validus**: Frank AI (Oct 2025) adds NLP/LLM. Enterprise, on-premise available
- **ComplyAdvantage**: $99.99/mo starter. Best entry-level AML API. ComplyLaunch program for startups
- **Unit21**: No-code compliance. Nexo achieved 93% false positive reduction
- **Feedzai**: Enterprise AI-native. Federated learning (Feedzai IQ) is unreplicable moat

### SAR Automation
- FinCEN confirmed AI-assisted SAR drafting is acceptable (Oct 2025 FAQ)
- Human-in-the-loop REQUIRED at approval stage
- EU AI Act (Aug 2026): compliance AI = high-risk, requires human oversight
- moov-io/fincen: open-source Go library for FinCEN BSA XML generation
- Time savings: 60-75% per SAR with AI drafting

### False Positive Benchmarks
- Legacy rule-based: 90-95% false positive
- AI-enhanced: 15-30% (Unit21/Bakkt: 15%)
- Best-in-class: 7-15% (HSBC Google Cloud: 60% alert reduction)

### On-Premise Open-Source Stack
- **Jube**: AGPLv3, real-time AML monitoring, Docker/K8s, self-hosted
- **Marble**: Open-source fraud/AML decision engine, self-hosted
- **GraphSense**: MIT license, blockchain analytics (requires significant hardware)
- **OpenSanctions**: Self-hostable sanctions/PEP screening
- **Ollama + local LLM**: SAR drafting on-premise

### Build vs License
- BUILD: SAR drafting, alert triage/classification, FinCEN XML filing (moov-io)
- LICENSE: Crypto blockchain risk scoring (vendor moat too strong on attribution)
- LICENSE: KYC identity verification (biometric = vendor only)
- HYBRID: Transaction monitoring (Jube for basic + TRM BLOCKINT API for crypto intel)
