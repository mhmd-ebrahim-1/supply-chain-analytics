# Power BI Project Guide

This directory contains the Power BI Project (`.pbip`), TMDL semantic model, PBIR report definition, and DAX library.

---

## Quick Start

1. Open Power BI Desktop (September 2024 or newer with PBIP / PBIR support enabled).
2. Open `Supply_Chain_Analytics.pbip`.
3. The report will load with all 4 pages, relationships, and DAX measures automatically.

---

## Directory Contents

| Component | Path | Description |
|---|---|---|
| **PBIP Project** | `Supply_Chain_Analytics.pbip` | Main project entry point for Power BI Desktop. |
| **PBIR Report** | `Supply_Chain_Analytics.Report/` | Git-friendly JSON report definitions (pages, visuals, bookmarks). |
| **TMDL Semantic Model** | `Supply_Chain_Analytics.SemanticModel/` | Git-friendly TMDL model definitions (tables, measures, relationships). |
| **Theme** | `SupplyChainTheme.json` | Report theme specification (colors, fonts, borders). |
| **DAX Measures** | `dax_measures.dax` | Standalone reference library of all production measures. |
| **Report Specs** | `report_pages_specification.md` | Layout, visual types, and field bindings for all 4 pages. |

---

## Model Benchmark Totals

Verify key metrics in Desktop:
- **Total Sales:** \$33,054,402.04
- **Total Profit:** \$3,966,907.39
- **Total Orders:** 65,752
- **Late Delivery Rate:** 54.8% (network) / 57.3% (eligible)
