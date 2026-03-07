# Crypto Investigation & Blockchain Forensics Tools — Landscape Report
# Saved from research agent output — March 3, 2026
# Full report captured from agent abee97ccbcfc46d4e

See full agent output at: /private/tmp/claude-502/-Users-xbtsupernode-Work/tasks/abee97ccbcfc46d4e.output

## Key Findings Summary

### Enterprise Tier (Not for Coldstorm to license directly)
- **Chainalysis**: Market leader. 1B+ clustered addresses, 65K-107K+ entities. $100K-$500K+/yr. 94.85% TPR validated at USENIX 2025. Cloud-only. Agent-readiness: Low-Medium (KYT API only)
- **TRM Labs**: 2.4B labeled addresses, 100+ chains. "Glass Box" attribution. Avg contract $693K. Agent-readiness: Medium-High
- **Elliptic**: 50+ chains, 300M screenings/quarter. Strong cross-chain. Enterprise only. Agent-readiness: Medium-High
- **CipherTrace**: DEAD. Mastercard shut down key products March 2024. Remove from all analysis.

### Agent-Ready Platforms (Coldstorm's build stack)
- **AnChain.AI**: HIGHEST agent-readiness. Production MCP server, free API key, open-source AML MCP, agentic workflows (ReAct), x402 payments. 40 chains, $870M+ in seizures supported. FREE ENTRY.
- **Arkham Intelligence**: 800M+ labels, developer API with SQL, Oracle (ChatGPT-style), freemium. Best free label database.
- **Nansen**: MCP server, 500M+ labels, Smart Money tracking. $69/mo (95% price cut Sept 2025). Investment-focused, not forensics.
- **Bitquery**: GraphQL API, 40+ chains, Coinpath fund tracing (closest open equivalent to Chainalysis fund flow). Credit-based.
- **Dune Analytics**: SQL over 70+ chains, 700K+ community dashboards. $399/mo Plus tier. Build anything custom.

### The Data Moat — Honest Assessment
Chainalysis moat has 4 layers:
1. Ground truth attribution (manually verified address-to-entity mapping)
2. Proprietary clustering heuristics (hundreds, service-specific)
3. Customer feedback loop (exchanges sharing deposit addresses — self-reinforcing)
4. OSINT harvesting at scale (dark web + clear web)

What you CAN replicate: basic clustering, OFAC screening, known exchange identification, community labels
What you CANNOT replicate: service-specific heuristics, customer validation loop, court-admissible attribution, dark web OSINT at scale

### Accuracy Comparison
| Scenario | Open-Source Agent | Enterprise Tool |
|---|---|---|
| OFAC SDN check | ~100% | ~100% |
| Known exchange detection | 70-85% | 90-95%+ |
| Illicit activity detection | 30-50% | 85-95% |
| End-to-end cross-chain | 60-70% | 90%+ |

### Recommended Agent Stack
**MVP (Free-$500/mo):** AnChain.AI MCP + Arkham API + Etherscan V2 + Blockstream Esplora + OFAC SDN
**Production ($500-$1,500/mo):** Add Dune Plus ($399) + Bitquery + Nansen ($69)
**Enterprise (when client pays):** AnChain.AI enterprise or Chainalysis KYT

### Critical Discovery: AnChain.AI
- Only enterprise-trusted forensics platform with production MCP server
- Free entry tier (no credit card)
- Open-source at github.com/AnChainAI/aml-mcp
- Supported $870M+ in seizures (including $65M KyberSwap DOJ case Feb 2025)
- This is Coldstorm's starting point for System 3
