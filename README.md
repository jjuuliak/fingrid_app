# fingrid_app - Fingrid Open Data CLI

A small Python App that fetches electricity-related open data from Fingrid and displays the results as either a table in the terminal or a Matplotlib plot.

## Features
- Select dataset by ID (e.g. 75 for wind power generation).
- Query a time range using UTC ISO-8601 timestamps (format 2026-02-01T00:00:00Z)
- Output as terminal table or Matplotlib plot
- Error handling (missing API key, network, empty data)

## Prerequisites
- Python 3.10+
- A Fingrid Open Data API key

## Get an API Key
1. Register/login at Fingrid Open Data portal.
2. Create an API key in the developer portal.
3. Copy the API key, it will be set as an environmental variable as 'API_KEY'.

## Installation

### Windows Powershell
# In the project folder (fingrid_app)
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

## macOS / Linux (not tested)
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

## Configure your API key
# Windows PowerShell
```$env:API_KEY="YOUR_FINGRID_KEY"```

# macOs / Linux
export API_KEY="YOUR_FINGRID_KEY"

# plot
python app.py --dataset-id 75 `
  --start 2026-02-07T10:00:00Z `
  --end   2026-02-07T12:00:00Z `
  --format plot `
  --ylabel "MW"

# table
python app.py --dataset-id 75 `
  --start 2026-02-07T10:00:00Z `
  --end   2026-02-07T12:00:00Z `
  --format table

# result
                             value
time
2026-02-07 10:00:00+00:00  904.289
2026-02-07 10:15:00+00:00  861.870
2026-02-07 10:30:00+00:00  808.997
2026-02-07 10:45:00+00:00  742.557
2026-02-07 11:00:00+00:00  697.796
2026-02-07 11:15:00+00:00  662.231
2026-02-07 11:30:00+00:00  627.535
2026-02-07 11:45:00+00:00  603.730


## Project structure
fingrid_app/
├─ app.py                     # CLI entry point (dataset-only)
├─ config.py                  # API key + HTTP settings
├─ services/
│  └─ dataset_client.py       # Calls data.fingrid.fi dataset API
├─ core/
│  └─ processing.py           # Normalize rows → DataFrame, resampling
├─ ui/
│  ├─ table.py                # Pretty terminal tables
│  └─ viz.py                  # Matplotlib plots
├─ utils/
│  └─ errors.py               # Custom exceptions
└─ requirements.txt