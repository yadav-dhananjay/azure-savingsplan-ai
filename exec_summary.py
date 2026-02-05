
from typing import Dict
import pandas as pd
import requests


def build_ai_prompt(metrics: Dict, forecast_df: pd.DataFrame, sub_summary: pd.DataFrame) -> str:
    avg_util = metrics.get("utilization_pct", 0.0)
    unused = metrics.get("unused", 0.0)

    if not forecast_df.empty:
        try:
            start = forecast_df["yhat"].iloc[0]
            end = forecast_df["yhat"].iloc[-1]
            if start > 0:
                forecast_growth = ((end - start) / start) * 100
            else:
                forecast_growth = 0.0
        except Exception:
            forecast_growth = 0.0
    else:
        forecast_growth = 0.0

    sub_lines = []
    if not sub_summary.empty:
        for _, row in sub_summary.iterrows():
            sub_lines.append(f"- {row['subscription_name']}: ${row['total_cost']:.2f} in period")
    sub_text = "
".join(sub_lines) if sub_lines else "(No subscription cost data available)"

    prompt = f"""
You are a senior cloud financial management and FinOps expert.

Azure Savings Plan context:
- Average utilization: {avg_util:.2f}%
- Unused commitment (approx): ${unused:.2f}
- Forecasted cost growth over the forecast window: {forecast_growth:.2f}%

Subscription cost distribution (current period):
{sub_text}

Write a concise executive summary for IT and Finance leadership with:
1. A 2–3 sentence high-level summary of current Savings Plan performance.
2. 4–6 bullet-point key findings (utilization patterns, weekend/weekday behavior if visible, subscription drivers, forecast observations).
3. 3–5 actionable recommendations to optimize Savings Plan commitment and workload placement.
4. A short section called "Risks to monitor" with 2–3 bullets about over-/under-commitment risk and forecast uncertainty.
5. A rough statement of potential monthly savings if obvious (you may approximate based on utilization and unused commitment).

Use clear, non-technical language suitable for executives.
"""

    return prompt


def generate_ai_summary(prompt: str, cfg_aoai: Dict) -> str:
    endpoint = cfg_aoai.get("endpoint")
    api_key = cfg_aoai.get("api_key")
    deployment = cfg_aoai.get("deployment", "gpt-4o")

    if not endpoint or not api_key:
        return "Azure OpenAI configuration missing or incomplete. Please set endpoint and api_key in config.yaml."

    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2024-02-15-preview"

    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    body = {
        "messages": [
            {"role": "system", "content": "You are a FinOps executive advisor."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    resp = requests.post(url, headers=headers, json=body, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    try:
        content = data["choices"][0]["message"]["content"]
    except Exception:
        content = "Unable to parse Azure OpenAI response. Raw response: " + str(data)[:2000]

    return content
