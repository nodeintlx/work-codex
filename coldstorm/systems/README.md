# Coldstorm AI — Production Systems Index
## 5 AI Compliance & Investigation Systems
### Last Updated: 2026-03-03

| System | Name | Status | File | Daily Cost |
|--------|------|--------|------|------------|
| 1 | Litigation Intelligence Engine | Production (active) | system-1-litigation-engine.md | Cloud LLM usage only |
| 2 | Executive Operations Agent | Production (active) | system-2-chief-of-staff.md | Cloud LLM + MCP servers |
| 3 | Crypto Transaction Tracer | Production-ready | system-3-crypto-tracer.md | $0-$1,500/mo |
| 4 | Due Diligence Report Automator | Production-ready | system-4-dd-automator.md | $350-$500/mo |
| 5 | Compliance Monitoring & Alert Triage | Production-ready | system-5-compliance-monitor.md | $0-$500/mo |

## Deployment Modes
- **Cloud**: Claude API / GPT-4 + external data source APIs
- **On-Premise**: Ollama (Llama 3.3 / Mistral / DeepSeek) + self-hosted tools — zero data exposure
- **Hybrid**: LLM on cloud, sensitive data local, only non-PII identifiers sent externally

## Architecture & Research Documentation
- System definitions: ../docs/five-ai-systems-definition-2026-03-03.md
- Crypto forensics landscape: ../../knowledge/crypto-blockchain-forensics-landscape-2026-03-03.md
- OSINT/DD automation: ../../knowledge/osint-due-diligence-automation-research-2026-03-03.md
- Compliance/SAR automation: ../../knowledge/compliance-monitoring-sar-automation-research-2026-03-03.md

## Key Discovery: AnChain.AI MCP
- Only enterprise-trusted forensics platform with production MCP server
- Free entry tier, open-source at github.com/AnChainAI/aml-mcp
- Starting point for Systems 3 and 5
