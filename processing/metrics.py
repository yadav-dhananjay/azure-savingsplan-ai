
from typing import Dict
import pandas as pd


def compute_utilization_metrics(usage_df: pd.DataFrame, hourly_commitment: float) -> Dict:
    if usage_df.empty:
        return {
            "hourly_commitment": hourly_commitment,
            "used": 0.0,
            "unused": hourly_commitment,
            "utilization_pct": 0.0,
        }

    # Approximate: assume commitment applies every hour and usage_df contains daily total cost.
    total_used = usage_df["cost"].sum()

    # For reporting, treat commitment as reference, not exact billing math.
    utilization_pct = 0.0
    unused = 0.0
    if hourly_commitment > 0:
        utilization_pct = min(100.0, (total_used / (hourly_commitment * 24 * max(1, usage_df["date"].nunique()))) * 100)
        # This is a heuristic; real unused computation requires Savings Plan utilization API.

    metrics = {
        "hourly_commitment": round(hourly_commitment, 2),
        "used": round(total_used, 2),
        "unused": round(unused, 2),
        "utilization_pct": round(utilization_pct, 2),
    }

    return metrics


def build_subscription_summary(usage_df: pd.DataFrame) -> pd.DataFrame:
    if usage_df.empty:
        return usage_df
    summary = (
        usage_df.groupby("subscription_name")["cost"].sum().reset_index()
    )
    summary.rename(columns={"cost": "total_cost"}, inplace=True)
    return summary
