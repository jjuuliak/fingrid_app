import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def plot_timeseries(df: pd.DataFrame, title: str, ylabel: str = "Value"):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["value"], color="#EE47DA", linewidth=1.8, label="Value")
    plt.title(title)
    plt.xlabel("Time (UTC)")
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.legend()
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M", tz=df.index.tz))
    plt.tight_layout()
    plt.show()