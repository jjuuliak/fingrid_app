import os

# Accept either env var name
FINGRID_API_KEY = os.getenv("API_KEY") or os.getenv("FINGRID_API_KEY")

# HTTP settings
HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", "20"))       # seconds
HTTP_RETRIES = int(os.getenv("HTTP_RETRIES", "3"))
HTTP_BACKOFF = float(os.getenv("HTTP_BACKOFF", "1.5"))    # multiplier for simple backoff
USER_AGENT = os.getenv("USER_AGENT", "fingrid-dataset-cli/1.0")