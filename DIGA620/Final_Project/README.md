# DIGA620 Final Project

This is code for my DIGA620 Final Project. `download_data.py` downloads data from
[NOAA's API](https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted).

## Stations
Data is downloaded for 6 weather stations defined in the code.

## API Token
The code requires an API token available through NOAA's API service. Put your own in a
file called `noaa_token.py` in the format `token = {"token": "#########"}`.

## Data Output
Data is output in JSON format with the structure:
```JavaScript
station_data = {
    "station_id": station_id,
    "station_name": station,
    "latitude": -999,
    "longitude": -999,
    "elevation": -999,
    "dates": {
        "2026-01-01": {
            "precip": 0,
            "max_temp": 100,
            "min_temp": 0
        }
        "2026-01-02": {
            "precip": 1,
            "max_temp": 90,
            "min_temp": 10
        }
    }
}
```
