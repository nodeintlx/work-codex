# Facts and Numbers Claim Audit

Source page:
- `https://www.nrgbloom.com/facts-and-numbers`
- Local capture: `nrg-bloom/capital-engine/facts/facts-and-numbers-2026-03-26.html`
- Checked on: `2026-03-26`

This audit separates claims that were strong enough to ingest today from claims that
need tighter wording or stronger proof before they should appear in investor or social
content.

## Verified And Ingested

- `Ogboinbiri operations since February 2025`
  Backed by internal operating documents and repeated site-brief language.
- `Ogboinbiri described as 1.5 MW operational`
  Backed by internal call-prep materials plus the investor page dataset markup.
- `Global data-centre electricity demand could more than double by 2030`
  Tightened from the page's broader "capacity must double" wording to match IEA phrasing.
- `Nigeria still has a severe electricity-access and power-reliability gap`
  Backed by World Bank materials describing roughly 85-90 million people without access and
  roughly $26-29 billion in annual economic losses.
- `Nigeria's grid regularly delivers only a fraction of nominal national capacity`
  Tightened from the page's exact `14 GW / 4-5 GW` framing to a broader, better-sourced
  delivery-gap statement using IEA and World Bank materials.
- `NGFCP has moved into a permit-backed execution phase`
  Backed by NUPRC plus secondary reporting on 28 permits, 49 sites, 42 bidders, and nearly
  3 GW of power potential.
- `Nigeria's third-party data-centre market remains structurally small`
  Backed by market-intelligence coverage citing roughly `65.8 MW` live and `327.8 MW`
  planned or under construction.
- `Green Flare has the largest public flare-to-compute announcement currently visible in Nigeria`
  Backed by multiple industry sources on its `53 MW` plan.
- `Crusoe validated flare-to-compute at scale, then sold its mining operation to NYDIG`
  Backed by Crusoe, CNBC, and DCD.

## Tightened Before Ingestion

- `Global data center capacity must double by 2030`
  Rewritten as `electricity demand from data centres could more than double by 2030`.
  Reason: the best primary source found was IEA demand language, not capacity language.
- `Nigeria has 14 GW installed capacity but delivers only 4-5 GW`
  Rewritten as a delivery-gap fact.
  Reason: the page's exact phrasing is directionally right, but the strongest corroboration
  found across World Bank and IEA materials was better framed around available/delivered power.
- `The market is 3 GW`
  Rewritten as `NGFCP reporting points to nearly 3 GW of power potential`.
  Reason: the stronger sourcing supports programme potential, not a precise TAM claim.

## Withheld Pending Stronger Proof

- `Built for $47K`
  Not ingested. Current support is too thin for public authority content.
- `Commercial partnerships under review with Oando and Heirs Energies`
  Oando is clearly supported internally; Heirs support is not yet strong enough for public use.
- `Canurta as first HPC pilot client`
  Current repo evidence supports relationship context, but not the full public claim as written.
- `25% power allocated to host community`
  Internal evidence supports community economics, not a clean public power-allocation fact.
- `Verra VM0029 / carbon-credit pricing stack`
  Current evidence is not strong enough to present this as an active, investor-ready fact.
- `Africa has 211 data centers for 1.4 billion people`
  Directionally plausible, but the source chain was weaker than the rest of the registry.
- `$22B/year on backup generators`
  Not ingested until a cleaner primary citation is captured.

## Operating Rule Going Forward

The investor page can keep strong narrative framing, but anything that enters the Codex fact
registry should be one of:

- directly corroborated by internal records
- corroborated by at least 3 sources
- and, for public or hybrid claims, backed by at least 2 authoritative external sources
