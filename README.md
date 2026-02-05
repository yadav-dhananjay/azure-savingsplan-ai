
# Azure Savings Plan – AI FinOps Pipeline

This project automates Azure Savings Plan analysis across multiple subscriptions, generates a finance-ready Excel report, and adds an AI-written executive summary.

## Features
- Multi-subscription Azure Cost Management ingestion
- Savings Plan utilization and efficiency metrics (configurable commitment)
- 60-day cost forecasting using Prophet
- Excel report with multiple sheets:
  - Usage_Daily
  - Subscription_Summary
  - SavingsPlan_Utilization
  - Forecast_60_Days
  - Executive_Summary
  - AI_Executive_Summary
- Azure OpenAI integration for narrative insights

## Quick start
1. Create a Python virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update `config.yaml` with your Azure and Azure OpenAI details.
4. Run the pipeline:
   ```bash
   python main.py
   ```
5. Open `outputs/azure_savings_plan_report.xlsx` in Excel or Power BI.
