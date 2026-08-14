import httpx

url = "https://api.open-meteo.com/v1/forecast"


params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "hourly": "temperature_2m",
}

response = httpx.get(
    url,
    params=params,
    timeout=10
    
)

print(response.status_code)

print(response.url)

data = response.json()

print(data)