
from typing import Dict
import pandas as pd
from azure.mgmt.costmanagement import CostManagementClient
from azure.identity import ClientSecretCredential


def fetch_cost_for_subscription(credential: ClientSecretCredential, sub_id: str, sub_name: str) -> pd.DataFrame:
    client = CostManagementClient(credential)

    query = {
        "type": "Usage",
        "timeframe": "MonthToDate",
        "dataset": {
            "granularity": "Daily",
            "aggregation": {
                "cost": {"name": "Cost", "function": "Sum"},
            },
        },
    }

    result = client.query.usage(
        scope=f"/subscriptions/{sub_id}",
        parameters=query,
    )

    df = pd.DataFrame(result.rows, columns=[c.name for c in result.columns])

    # Normalize
    if "UsageDate" in df.columns:
        df["date"] = pd.to_datetime(df["UsageDate"])
    else:
        raise ValueError("Expected column 'UsageDate' in cost query result")

    if "Cost" in df.columns:
        df["cost"] = df["Cost"]
    else:
        raise ValueError("Expected column 'Cost' in cost query result")

    df["subscription_id"] = sub_id
    df["subscription_name"] = sub_name

    return df[["date", "cost", "subscription_id", "subscription_name"]]
