import httpx
from dotenv import load_dotenv

load_dotenv()

import os


urlforecast = os.getenv("urlforecast")


if not urlforecast:
    raise ValueError("The 'url' environment variable is missing or not set.")



params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "hourly": "temperature_2m",
}

response = httpx.get(urlforecast, params=params, timeout=10)

print(response.status_code)

print(response.url)

data = response.json()

print(data)
