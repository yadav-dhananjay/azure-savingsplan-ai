
import pandas as pd
from prophet import Prophet


def prepare_forecast_base(usage_df: pd.DataFrame) -> pd.DataFrame:
    if usage_df.empty:
        return pd.DataFrame(columns=["date", "cost"])
    base = usage_df.groupby("date")["cost"].sum().reset_index()
    return base


def prophet_forecast(base_df: pd.DataFrame, days: int) -> pd.DataFrame:
    if base_df.empty:
        return pd.DataFrame(columns=["ds", "yhat"])

    prophet_df = base_df.rename(columns={"date": "ds", "cost": "y"})

    model = Prophet(daily_seasonality=True, weekly_seasonality=True)
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=int(days))
    forecast = model.predict(future)

    return forecast[["ds", "yhat"]]
