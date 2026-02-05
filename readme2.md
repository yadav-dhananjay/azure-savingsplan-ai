# Azure Savings Plan – AI FinOps Pipeline

This project automates analysis of **Azure Savings Plans for compute**, pulling usage across multiple subscriptions, generating a finance‑friendly Excel report, and adding an AI‑written executive summary using Azure OpenAI. [web:19][web:22]

---

## 1. What this project does

- Collects cost and usage data from Azure Cost Management for one or more subscriptions. [web:14][web:20]
- Aggregates daily spend and builds per‑subscription summaries.
- Applies a configurable Savings Plan hourly commitment to derive heuristic utilization metrics.
- Generates a 60‑day cost forecast using Prophet.
- Calls Azure OpenAI to generate an executive narrative (summary, key findings, recommendations, risks). [web:21]
- Produces a multi‑sheet Excel workbook suitable for Finance and Power BI.

Output file:

- `outputs/azure_savings_plan_report.xlsx`

Sheets inside: `Usage_Daily`, `Subscription_Summary`, `SavingsPlan_Utilization`, `Forecast_60_Days`, `Executive_Summary`, `AI_Executive_Summary`. [code_file:11]

---

## 2. Architecture overview

**Core flow**

1. Authenticate to Azure using a service principal. [code_file:7]
2. Query Cost Management **Usage** for each configured subscription (Month‑to‑Date, daily granularity). [code_file:8][web:14]
3. Concatenate all subscriptions into a single usage dataset.
4. Compute Savings Plan metrics using the configured hourly commitment. [code_file:10][web:19]
5. Build a daily total time series and run Prophet to forecast future costs. [code_file:9]
6. Build a FinOps‑oriented prompt and call Azure OpenAI chat completions for an executive summary. [code_file:6][web:21]
7. Write all data and narratives into a single Excel file. [code_file:11]

**Key components**

| Path | Purpose |
| --- | --- |
| `main.py` | Orchestrates end‑to‑end pipeline |
| `config.yaml` | Azure, subscriptions, Savings Plan commitment, forecast, Azure OpenAI config |
| `auth/azure_auth.py` | Service principal auth + ARM token helper |
| `data/cost_query.py` | Cost Management Usage API (per subscription) |
| `processing/metrics.py` | Utilization metrics + subscription summary |
| `forecasting/prophet_forecast.py` | Prophet‑based daily forecast |
| `ai/exec_summary.py` | Prompt builder + Azure OpenAI call |
| `reporting/excel_report.py` | Excel writer with 6 sheets |
| `outputs/` | Generated Excel report |

---

## 3. Prerequisites

- Python 3.9+ (recommended)
- Azure subscription(s) with Cost Management data enabled. [web:14]
- Service principal with at least:
  - `Cost Management Reader` or `Reader` on each subscription. [web:14]
- Azure OpenAI resource with a chat model deployment (for example, `gpt-4o`). [web:21]

Install Python dependencies:

```bash
pip install -r requirements.txt




4. Configuration
Edit config.yaml:

text
tenant_id: "<TENANT_ID>"
client_id: "<CLIENT_ID>"
client_secret: "<CLIENT_SECRET>"

subscriptions:
  - id: "<SUBSCRIPTION_ID_1>"
    name: "Prod-Subscription"
  - id: "<SUBSCRIPTION_ID_2>"
    name: "NonProd-Subscription"

savings_plan_hourly_commitment: 120.0   # set to your Savings Plan hourly commitment

forecast:
  days: 60

azure_openai:
  endpoint: "https://<your-aoai-endpoint>.openai.azure.com/"
  api_key: "<AZURE_OPENAI_KEY>"
  deployment: "gpt-4o"
Notes:

savings_plan_hourly_commitment reflects your Azure Savings Plan hourly commitment; this repo uses it to approximate utilization and unused commitment for reporting. [web:19][web:22]

endpoint must be your Azure OpenAI endpoint URL.

deployment must match an existing chat model deployment (for example, gpt-4o or equivalent). [web:21]

5. Running the pipeline
From the repo root:

bash
python main.py
The script will: [code_file:4]

Load configuration from config.yaml.

Use ClientSecretCredential for Azure AD auth. [code_file:7]

Call the Cost Management Query API per subscription (Month‑to‑Date, daily). [code_file:8][web:14]

Compute utilization metrics based on your Savings Plan commitment. [code_file:10]

Generate a 60‑day cost forecast. [code_file:9]

Call Azure OpenAI to produce an AI executive summary. [code_file:6][web:21]

Write outputs/azure_savings_plan_report.xlsx. [code_file:11]

On success, you’ll see a console message with the report path.

6. Excel report structure
outputs/azure_savings_plan_report.xlsx contains: [code_file:11]

Usage_Daily

Columns: date, cost, subscription_id, subscription_name

Daily cost per subscription (Month‑to‑Date; extendable in code for other periods). [code_file:8]

Subscription_Summary

Columns: subscription_name, total_cost

Aggregated total cost per subscription. [code_file:10]

SavingsPlan_Utilization

Single row with: hourly_commitment, used, unused, utilization_pct (heuristic). [code_file:10]

Commitment is a configurable reference; precise utilization requires Savings Plan utilization APIs. [web:19]

Forecast_60_Days

Columns: date, forecast_cost

Daily cost forecast using Prophet with daily and weekly seasonality. [code_file:9]

Executive_Summary

Simple KPI table showing commitment, total used, approximate unused, and utilization %. [code_file:11]

AI_Executive_Summary

Single column, multi‑row text with AI‑generated summary, key findings, recommendations, and risks. [code_file:6][code_file:11]

You can use this workbook directly in Excel or as a data source in Power BI.

7. How the AI executive summary works
The AI layer (ai/exec_summary.py) does the following: [code_file:6]

Builds a prompt using:

Utilization % and unused commitment (approx).

Subscription cost distribution.

Forecasted cost growth over the forecast window.

Sends a chat completion request to Azure OpenAI using the configured deployment. [web:21]

Receives a structured narrative with:

High‑level summary.

Key findings.

Recommendations.

Risks to monitor.

Writes each line into the AI_Executive_Summary sheet as a row. [code_file:11]

If Azure OpenAI configuration is missing or invalid, the sheet will contain a diagnostic message instead of an empty report. [code_file:6]

8. Customization ideas
You can easily extend this project to:

Change the Cost Management timeframe (e.g., last 30 days, last month). [web:14][web:17]

Add Savings Plan utilization API calls for more accurate commitment vs. usage calculations. [web:19]

Add PAYG vs Savings Plan breakdowns to distinguish covered vs uncovered spend. [web:19][web:22]

Schedule regular execution via Azure Functions, GitHub Actions, or other automation.

Feed the Excel outputs into a Power BI model for interactive dashboards.

9. Disclaimer
This project uses heuristics to approximate Savings Plan utilization based on cost data and a configured hourly commitment. For precise billing behavior (discount allocation, unused commitment, and detailed utilization), refer to Azure’s official Savings Plan and Cost Management documentation. [web:19][web:14]

text
undefined
azure_savingsplan_ai_full.zip
azure_savingsplan_ai_full.zip