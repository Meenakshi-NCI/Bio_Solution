# dummy-weather-api

A dummy Go HTTP service that accepts fake weather sensor readings and returns a rain probability prediction.

## Endpoint

`POST /predict`

### Request body

```json
{
  "readings": [
    {
      "timestamp": "2024-01-01T12:00:00Z",
      "temperature": 18.5,
      "humidity": 75.0,
      "pressure": 1012.0,
      "wind_speed": 12.3
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | string (ISO 8601) | Time of the reading |
| `temperature` | float | °C |
| `humidity` | float | % relative humidity |
| `pressure` | float | hPa |
| `wind_speed` | float | km/h |

### Response

```json
{
  "rain_probability": 0.42,
  "recommendation": "Possible showers - keep an eye on the sky",
  "readings_count": 1
}
```