# NEO overhead: sources

Pulled 2026-11-09 (HST) directly from SEC EDGAR: XBRL company facts (`data.sec.gov`) and the
filing documents (`www.sec.gov`). SEC requires a declared User-Agent; requests without one get
403. Scripts: `capabilities/neo-overhead/pull_xbrl.py` and `pull_10k.py`. Every figure in the
deck is reported in one of the filings below, or is arithmetic on reported figures.

## NeoGenomics

| Figure | Value | Where |
|---|---|---|
| Sales FY2025 / 2024 / 2023 / 2022 / 2021 | $727.3M / $660.6M / $591.6M / $509.7M / $484.3M | 10-Ks, income statement (XBRL) |
| G&A FY2025 / 2024 / 2023 / 2022 / 2021 | $273.3M / $259.7M / $243.1M / $243.4M / $221.3M | 10-Ks (XBRL) |
| Sales & marketing FY2025 | $92.0M | FY2025 10-K |
| Stock pay by line, FY2025 | G&A $34.3M, S&M $3.1M, R&D $2.5M, cost of revenue $1.4M; total $41.3M | FY2025 10-K, Note 9 |
| Depreciation by line, FY2025 | G&A $20.8M, cost of revenue $13.2M, R&D $2.0M, S&M $0.1M; total $36.1M | FY2025 10-K, Note 5 |
| Other G&A (ex D&A and stock pay) | $205.4M | FY2025 10-K, Note 17 segment table |
| Amortization in G&A | $12.8M (= 273.3 − 205.4 − 34.3 − 20.8; cross-check: $31.8M total − $18.9M in cost of revenue) | Derived from Notes 5, 9, 17 |
| One-offs | IP litigation $11.283M, acquisition & integration $7.266M, CEO transition $3.500M; 2024 total $26.1M | FY2025 10-K, adjusted EBITDA reconciliation |
| Pathline integration in G&A | $4.7M | FY2025 10-K, acquisition note |
| G&A drivers 2025 | pay +11.5, software +8.0, transaction +1.4, legal/professional −2.1, equipment −1.8, travel −1.3, amortization −1.0, facilities −0.5 | FY2025 10-K MD&A |
| Receivables, year-end 2025 | $159.2M (≈80 days of sales) | FY2025 10-K balance sheet |
| Operating lease cost | $9.6M | FY2025 10-K, Note 6 |
| Headcount | ~2,500 FTEs (2025), ~2,200 (2024) | FY2025 and FY2024 10-Ks, human capital |
| Executive cash pay | $6.68M (salary + bonus + non-equity incentive + other, 7 named officers) | 2026 proxy (DEF 14A, filed 2026-04-06), Summary Compensation Table |
| Director cash fees | $0.62M | 2026 proxy, director compensation table |
| Deloitte fees | $2.77M total, of which audit $1.98M | 2026 proxy, auditor fees |
| Q3 2026 G&A 32.1% of sales; ~93 days to collect; CEO succession | | Q3 2026 results, via v2 deck |

## Peers, FY2025 ($M)

| Company | Sales | SG&A | S&M | G&A | Stock pay | Stock pay in G&A | Receivables |
|---|---|---|---|---|---|---|---|
| Quest | 11,035.0 | 1,967.0 | – | – | 88.0 | – | 1,408.0 (reported DSO 48) |
| Labcorp | 13,951.7 | 2,216.3 | – | – | 125.8 | – | 2,103.8 |
| Exact Sciences | 3,247.0 | 1,938.9 | 1,050.2 | 888.7 | 217.7 | 96.3 | 298.7 |
| Natera | 2,306.1 | 1,177.3 | – | – | 354.4 | – | 296.5 |
| Myriad | 824.5 | 537.6 | 280.8 | 256.8 (incl. $34.7M amortization) | 35.2 | 22.1 | 115.3 |
| Veracyte | 517.1 | 211.0 | 100.2 | 110.8 | 43.6 | 25.1 | 44.7 |
| Castle | 344.2 | 229.3 | 138.1 | 91.2 | 45.9 | 17.4 | 43.4 |
| Fulgent | 322.7 | 160.1 | 43.4 | 116.7 (incl. $14.5M liability accrual) | 39.6 | 16.5 | 84.8 |

Sales, SG&A, S&M, G&A, stock pay and receivables come from XBRL company facts. Stock pay in G&A,
Myriad's amortization, Fulgent's accrual and Quest's DSO come from the 10-K text.

## Not public

- NeoGenomics' G&A by function (billing, IT, finance and so on). It would need internal cost-center data.
- Quest's and Labcorp's split of SG&A into selling, billing and admin.
