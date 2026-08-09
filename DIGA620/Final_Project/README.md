# DIGA620 Final Project

This is code for my DIGA620 Final Project. `download_data.py` downloads data from
[NOAA's API](https://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted).

## Stations
Data is downloaded for 6 weather stations defined in the code.

## API Token
The code requires an API token available through NOAA's API service. Put your own in a
file called `noaa_token.py` in the format `token = {"token": "#########"}`.

## Data Output
Data is output in 2 JSON files. The `stations_info.json` output has the structure:
```JavaScript
{
    "station": {
        "station_id": station_id,
        "station_name": station,
        "latitude": -999,
        "longitude": -999,
        "elevation": -999
    }
}
```
The `weather_data.json` output has the structure:
```JavaScript
{
    "2026-01-01T00:00:00": [
        ["####", 1, 100, 10],
        ["####", 2, 200, 20],
        ["####", 3, 300, 30],
        ["####", 4, 400, 40]
    ]
}
```
where each date element is a list of lists, each of those lists being in the order:
 1. station_id
 2. precipitation
 3. max_temp
 4. min_temp
