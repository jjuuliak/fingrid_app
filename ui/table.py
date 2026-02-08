import pandas as pd

def print_table(df: pd.DataFrame, rows: int = 20):
    # Display a neat snapshot
    pd.set_option("display.width", 140)
    pd.set_option("display.max_columns", 10)
    print(df.head(rows).to_string())
    if len(df) > rows:
        print(f"\n... ({len(df) - rows} more rows)")