import time
import requests
from typing import Any, Dict, List, Optional, Union

from config import FINGRID_API_KEY, HTTP_TIMEOUT, HTTP_RETRIES, HTTP_BACKOFF, USER_AGENT
from utils.errors import ConfigError, ApiError

BASE = "https://data.fingrid.fi/api"

class DatasetClient:
    """
    Client for the dataset portal API (data.fingrid.fi).

    Example:
      /datasets/{dataset_id}/data?startTime=...&endTime=...&format=json&locale=en&sortBy=startTime&sortOrder=asc
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or FINGRID_API_KEY
        if not self.api_key:
            raise ConfigError("Missing API key. Set API_KEY environment variable.")
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": self.api_key,
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
            "Cache-Control": "no-cache",
        })

    def get_dataset_data(self, dataset_id: int, start_iso: str, end_iso: str, locale: str = "en") -> List[Dict[str, Any]]:
        url = f"{BASE}/datasets/{dataset_id}/data"
        params = {
            "startTime": start_iso,
            "endTime": end_iso,
            "format": "json",
            "locale": locale,
            "sortBy": "startTime",
            "sortOrder": "asc",
        }

        last_err: Optional[Exception] = None
        for attempt in range(1, HTTP_RETRIES + 1):
            try:
                resp = self.session.get(url, params=params, timeout=HTTP_TIMEOUT)
                # If throttled, wait and retry
                if resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", "1"))
                    time.sleep(retry_after)
                    continue
                resp.raise_for_status()

                # Try to parse JSON safely
                try:
                    data: Union[List[Any], Dict[str, Any], str] = resp.json()
                except ValueError:
                    # Not JSON (unlikely with format=json) – raise with text preview
                    raise ApiError(f"Response is not JSON. First 200 chars: {resp.text[:200]}")

                # Normalize to a list of dicts
                if isinstance(data, list):
                    rows = data
                elif isinstance(data, dict):
                    # Some APIs wrap results; try common keys
                    rows = data.get("data") or data.get("results") or data.get("observations") or []
                else:
                    # A plain string (e.g., an error message) – raise a helpful error
                    raise ApiError(f"Unexpected response type: {type(data).__name__}. Preview: {str(data)[:200]}")

                # Guard against non-dict items in the list
                rows = [r for r in rows if isinstance(r, dict)]
                return rows

            except (requests.Timeout, requests.RequestException, ApiError) as e:
                last_err = e
                time.sleep(HTTP_BACKOFF * attempt)

        raise ApiError(f"Dataset API request failed after {HTTP_RETRIES} retries: {last_err}")