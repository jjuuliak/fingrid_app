import pandas as pd
from typing import List, Dict
from utils.errors import DataError

def to_timeseries(rows: List[Dict], value_field: str = "value") -> pd.DataFrame:
    if not rows:
        raise DataError("Empty data for the selected time window.")
    df = pd.DataFrame(rows)

    # Dataset API uses 'startTime'/'endTime' – normalize to 'start_time'
    ts_col = "startTime" if "startTime" in df.columns else ("start_time" if "start_time" in df.columns else None)
    if ts_col is None or value_field not in df.columns:
        raise DataError(f"Unexpected schema. Columns available: {list(df.columns)}")

    # Parse times & values
    df[ts_col] = pd.to_datetime(df[ts_col], utc=True, errors="coerce")
    df = df.dropna(subset=[ts_col]).set_index(ts_col).sort_index()
    df["value"] = pd.to_numeric(df[value_field], errors="coerce")
    df = df.dropna(subset=["value"])
    if df.empty:
        raise DataError("No numeric values after parsing.")
    # Use a unified index name for display
    df.index.name = "time"
    return df[["value"]]

def resample_timeseries(df: pd.DataFrame, rule: str = None, agg: str = "mean") -> pd.DataFrame:
    if not rule:
        return df
    if agg == "mean":
        out = df.resample(rule).mean()
    elif agg == "sum":
        out = df.resample(rule).sum()
    else:
        raise DataError(f"Unsupported aggregation: {agg}")
    return out.dropna(how="all")