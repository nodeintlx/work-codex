# Data Sheet — Nigeria Does Not Have a Power Shortage. It Has a Delivery Problem.

Brief slug: africa-power-myth
Hero stat: 14 GW of installed capacity in Nigeria. Roughly 4 GW actually delivered on an average day. The gap is not fuel. It is everything between the turbine and the socket.
Core thesis: Site the compute at the source and the transmission failure that defines Nigerian power stops being your risk and starts being your discount.

## Claims Used In The Post

- Hook claim: The lazy take is that Africa cannot power data centers. The real story is narrower and far more useful: Nigeria cannot move power, which is a completely different problem if you are willing to build at the source.
- Proof point 1: The IEA put Nigeria's installed generation capacity at 14 GW in 2024 with average daily available capacity of 4.14 GW. That is a delivery failure, not a fuel failure.
- Proof point 2: World Bank materials put roughly 85 to 90 million Nigerians without grid access, with the economic cost of poor supply estimated in the tens of billions of dollars a year.
- Proof point 3: In the same country, gas is being flared at the wellhead. The energy is present and already at surface. The wires are the thing that is missing.
- Contrarian take: Almost every argument for why African compute is impossible turns out, when you push on it, to be an argument about transmission. Behind-the-meter compute does not use transmission.

## Verified Facts

### nigeria_grid_delivery_gap
Recent institutional analyses describe Nigeria's grid as delivering only roughly 3-5 GW on average despite materially higher installed or nominal capacity.
Scope: external

Sources:
- [official_report] institutional | Electricity 2025
  URL: https://www.iea.org/reports/electricity-2025
  Excerpt: Nigeria’s installed generation capacity rose to 14 GW in 2024, but average daily available capacity was 4.14 GW.
  Checked: 2026-03-26
- [multilateral] institutional | Nigeria Power Sector Guarantees Project
  URL: https://documents1.worldbank.org/curated/en/193911617633470778/pdf/Nigeria-Power-Sector-Guarantees-Project.pdf
  Excerpt: The electricity produced and distributed within Nigeria hovers between 3 GW and 4 GW, peaking at 5 GW.
  Checked: 2026-03-26
- [multilateral] institutional | Nigeria Electrification Project
  URL: https://www.afdb.org/fileadmin/uploads/afdb/Documents/Project-and-Operations/PESR_NG_NIGERIA_ELECTRIFICATION_PROJECT_CORR_EN-final.pdf
  Excerpt: Nearly 14 GW... is generated through inefficient and costly generation solutions, showing how far real electricity demand outruns formal grid delivery.
  Checked: 2026-03-26

### nigeria_power_access_and_losses
Recent World Bank materials describe Nigeria as having the world's largest electricity access deficit, with roughly 85-90 million people lacking access and annual economic losses from poor power supply in roughly the $26-29 billion range.
Scope: external

Sources:
- [multilateral] institutional | The World Bank Approves Additional Financing to Consolidate the Gains of Nigeria's Power Sector Recovery Program
  URL: https://www.worldbank.org/en/news/press-release/2023/06/09/the-world-bank-approves-additional-financing-to-consolidate-the-gains-of-nigeria-s-power-sector-recovery-program
  Excerpt: Lack of access to the electricity grid affects 45 percent of the population (90 million people), making Nigeria the country with the largest number of people not connected to electricity.
  Checked: 2026-03-26
- [multilateral] institutional | Nigeria Distributed Access through Renewable Energy Scale-up (DARES) Program-for-Results
  URL: https://documents.worldbank.org/en/publication/documents-reports/documentdetail/099082124112015103/p17968714b12670871924f3b6c5d0ff4d8
  Excerpt: About 85 million Nigerians do not have access to electricity and economic losses due to poor electricity supply are estimated at US$26.2 billion.
  Checked: 2026-03-26
- [multilateral] institutional | Nigeria to Keep the Lights on and Power its Economy
  URL: https://www.worldbank.org/en/news/press-release/2020/06/23/nigeria-to-keep-the-lights-on-and-power-its-economy
  Excerpt: About 47% of Nigerians do not have access to grid electricity... the economic cost of power shortages in Nigeria is estimated at around $28 billion.
  Checked: 2026-03-26

### global_flaring_2024_151bcm
The World Bank's 2025 tracker said global gas flaring reached 151 bcm in 2024.
Scope: external

Sources:
- [official_dataset] institutional | Global Gas Flaring Data
  URL: https://www.worldbank.org/en/programs/gasflaringreduction/global-flaring-data
  Excerpt: Our estimates, derived from satellite data, show that 151 billion cubic meters (bcm) of associated gas was flared... in 2024.
  Checked: 2026-03-26
- [official_report] institutional | 2025 Global Gas Flaring Tracker Report
  URL: https://www.worldbank.org/en/programs/gasflaringreduction/publication/2025-global-gas-flaring-tracker-report
  Excerpt: In 2024, flaring surged by 3 billion cubic meters (bcm) to 151 bcm, the highest level since 2007.
  Checked: 2026-03-26
- [official_report] institutional | What is Gas Flaring?
  URL: https://www.worldbank.org/en/programs/gasflaringreduction/gas-flaring-explained
  Excerpt: The amount of gas currently flared each year – about 151 billion cubic meters (bcm).
  Checked: 2026-03-26

### modular_containerized_model
NRG Bloom's operating model is modular and containerized for remote energy-edge deployment.
Scope: internal

Sources:
- [internal_doc] internal
  Excerpt: Modular container-based data centers (Kifaru design).
- [internal_doc] internal
  Excerpt: We design and deploy modular data centers for emerging markets — specifically containerized computing infrastructure powered by stranded gas and flare gas in West Africa.
- [internal_doc] internal
  Excerpt: NRG Bloom deploys modular data centers at Oando's upstream sites.
