
from typing import Dict
import pandas as pd


def generate_excel_report(
    usage_df: pd.DataFrame,
    utilization_metrics: Dict,
    forecast_df: pd.DataFrame,
    ai_text: str,
    output_path: str,
) -> None:
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # Sheet 1 – Daily usage (all subscriptions)
        usage_df.to_excel(writer, sheet_name="Usage_Daily", index=False)

        # Sheet 2 – Subscription summary
        if not usage_df.empty:
            summary = (
                usage_df.groupby("subscription_name")["cost"].sum().reset_index()
            )
            summary.rename(columns={"cost": "total_cost"}, inplace=True)
        else:
            summary = pd.DataFrame(columns=["subscription_name", "total_cost"])

        summary.to_excel(writer, sheet_name="Subscription_Summary", index=False)

        # Sheet 3 – Savings Plan Utilization
        util_df = pd.DataFrame([utilization_metrics])
        util_df.to_excel(writer, sheet_name="SavingsPlan_Utilization", index=False)

        # Sheet 4 – Forecast
        if not forecast_df.empty:
            out_forecast = forecast_df.rename(columns={"ds": "date", "yhat": "forecast_cost"})
        else:
            out_forecast = pd.DataFrame(columns=["date", "forecast_cost"])
        out_forecast.to_excel(writer, sheet_name="Forecast_60_Days", index=False)

        # Sheet 5 – Executive Summary (numeric KPIs)
        exec_summary = pd.DataFrame(
            {
                "Metric": [
                    "Hourly Commitment (Configured)",
                    "Total Used Cost (Period)",
                    "Approx. Unused Commitment",
                    "Utilization % (Heuristic)",
                ],
                "Value": [
                    utilization_metrics.get("hourly_commitment"),
                    utilization_metrics.get("used"),
                    utilization_metrics.get("unused"),
                    utilization_metrics.get("utilization_pct"),
                ],
            }
        )
        exec_summary.to_excel(writer, sheet_name="Executive_Summary", index=False)

        # Sheet 6 – AI Executive Summary (text)
        lines = ai_text.split("
") if ai_text else ["No AI summary generated."]
        ai_df = pd.DataFrame({"AI Executive Summary": lines})
        ai_df.to_excel(writer, sheet_name="AI_Executive_Summary", index=False)
