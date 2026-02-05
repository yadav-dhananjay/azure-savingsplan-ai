
import os
import yaml
import pandas as pd

from auth.azure_auth import get_credential
from data.cost_query import fetch_cost_for_subscription
from processing.metrics import compute_utilization_metrics, build_subscription_summary
from forecasting.prophet_forecast import prepare_forecast_base, prophet_forecast
from ai.exec_summary import build_ai_prompt, generate_ai_summary
from reporting.excel_report import generate_excel_report


def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    cfg = load_config()

    credential = get_credential(cfg)

    # 1) Ingest usage for all subscriptions
    all_usage = []
    for sub in cfg.get("subscriptions", []):
        sub_id = sub["id"]
        sub_name = sub.get("name", sub_id)
        df = fetch_cost_for_subscription(credential, sub_id, sub_name)
        all_usage.append(df)

    if all_usage:
        usage_df = pd.concat(all_usage, ignore_index=True)
    else:
        usage_df = pd.DataFrame(columns=["date", "cost", "subscription_id", "subscription_name"])

    # 2) Compute metrics (heuristic, commitment from config)
    hourly_commitment = float(cfg.get("savings_plan_hourly_commitment", 0.0))
    utilization_metrics = compute_utilization_metrics(usage_df, hourly_commitment)

    # 3) Build subscription summary
    sub_summary = build_subscription_summary(usage_df)

    # 4) Forecast
    base_df = prepare_forecast_base(usage_df)
    forecast_days = int(cfg.get("forecast", {}).get("days", 60))
    forecast_df = prophet_forecast(base_df, forecast_days)

    # 5) AI Executive Summary via Azure OpenAI
    prompt = build_ai_prompt(utilization_metrics, forecast_df, sub_summary)
    ai_cfg = cfg.get("azure_openai", {})
    ai_text = generate_ai_summary(prompt, ai_cfg)

    # 6) Excel report
    os.makedirs("outputs", exist_ok=True)
    output_path = os.path.join("outputs", "azure_savings_plan_report.xlsx")

    generate_excel_report(
        usage_df=usage_df,
        utilization_metrics=utilization_metrics,
        forecast_df=forecast_df,
        ai_text=ai_text,
        output_path=output_path,
    )

    print(f"Report generated at: {output_path}")


if __name__ == "__main__":
    main()
