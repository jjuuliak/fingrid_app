import argparse
from services.dataset_client import DatasetClient
from core.processing import to_timeseries, resample_timeseries
from ui.table import print_table
from ui.viz import plot_timeseries

def main():
    p = argparse.ArgumentParser(description="Fingrid Dataset API viewer (dataset-only)")
    p.add_argument("--dataset-id", type=int, required=True, help="Dataset ID (e.g., 75 for wind)")
    p.add_argument("--start", required=True, help="UTC ISO8601, e.g., 2026-02-01T00:00:00Z")
    p.add_argument("--end", required=True, help="UTC ISO8601, e.g., 2026-02-02T00:00:00Z")
    p.add_argument("--format", choices=["table", "plot"], default="table")
    p.add_argument("--resample", default=None, help="Resample rule (e.g., 1h, 15min)")
    p.add_argument("--agg", choices=["mean", "sum"], default="mean")
    p.add_argument("--ylabel", default="Value")
    p.add_argument("--debug", action="store_true", help="Print first response items for troubleshooting")
    args = p.parse_args()

    try:
        client = DatasetClient()
        rows = client.get_dataset_data(args.dataset_id, args.start, args.end)

        if args.debug:
            print(f"[DEBUG] type(rows)={type(rows).__name__}, len={len(rows)}")
            if rows:
                print(f"[DEBUG] first item type: {type(rows[0]).__name__}")
                print(f"[DEBUG] first item preview: {str(rows[0])[:200]}")
            else:
                print("[DEBUG] rows is empty")

        # Normalize to time series DataFrame
        df = to_timeseries(rows, value_field="value")
        df = resample_timeseries(df, rule=args.resample, agg=args.agg)

        if args.format == "table":
            print_table(df)
        else:
            title = f"Dataset {args.dataset_id} — {args.start} → {args.end}"
            plot_timeseries(df, title=title, ylabel=args.ylabel)

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()