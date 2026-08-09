"""
Isaac List
DIGA620 Summer 2026
Final Project
"""

import requests, json, noaa_token

# Stations used for prototype
stations = {
    "LA CROSSE WEATHER FORECAST OFFICE": "GHCND:USC00474373",
    "PRAIRIE DU CHIEN MUNICIPAL AIRPORT": "GHCND:USW00004963",
    "SPARTA FORT MCCOY": "GHCND:USW00094940",
    "STEVENS POINT MUNICIPAL AIRPORT": "GHCND:USW00004895"
}

# NOAA API token
token = noaa_token.token

# Parameters for weather data retrieval
# - datasetid: daily summaries
# NOTE: stationid updated in retrieve_station_data for each station
# - startdate/enddate: 3-month period
# - datatypeid: retrieve just precipitation, max temp, min temp
# - units: use standard (F, inches)
# - limit: 1000 should cover all days (~90 records, 3 for each day)
parameters = {
    "datasetid": "GHCND",
    "stationid": "",
    "startdate": "2026-01-01",
    "enddate": "2026-03-31",
    "datatypeid": ["PRCP", "TMAX", "TMIN"],
    "units": "standard",
    "limit": "1000"
}

# Data endpoint
data_endpoint = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"

def retrieve_station_data(station: str, station_id: str) -> dict:
    """Retrieve static data for given station"""
    # Build structure
    station_data = {
        "station_id": station_id,
        "station_name": station,
        "latitude": -999,
        "longitude": -999,
        "elevation": -999
    }

    # Update URL path
    url = "https://www.ncei.noaa.gov/cdo-web/api/v2/stations/" + station_id

    # Request
    station_info = requests.get(url, headers = token)

    # Fill in lat, lon, elev data
    station_data["latitude"] = station_info.json()["latitude"]
    station_data["longitude"] = station_info.json()["longitude"]
    station_data["elevation"] = station_info.json()["elevation"]   

    return station_data

def retrieve_weather_data(station: str, station_id: str, weather_data: dict) -> dict:
    """
    Retrieve weather data for a given station, return in the format:

    {
        "01-01-2026": [
            ["abcdefg", 1, 100, 10],
            ["hijklmn", 2, 200, 20]   
        ]
    }

    Where each date is a list of lists, each list being in the order:
        station_id, precip, max_temp, min_temp
    to be split into separate columns once loaded in Excel.
    """
    # Update stationid in parameters
    parameters["stationid"] = station_id

    # Request
    station_weather = requests.get(data_endpoint, params = parameters, headers = token)

    # Parse list of dict results
    results: list = station_weather.json()["results"]

    # Fill in station_id, precip, max_temp, min_temp for each date

    # Results are in sets of 3 by date, thus the for loop jumping by 3's
    for i in range(0, len(results) - 2, 3):
        # Get 4 values from results: date will be key
        working_date = results[i]["date"]

        # Check if date already in object, if not then create with empty list
        if working_date not in weather_data.keys():
            weather_data[working_date] = []

        # These will be values, start with station_id
        working_date_data = [station_id, -999, -999, -999]

        # Since JSON order is inconsistent, add to my JSON in proper order
        for j in range(i, i+3):
            if results[j]["datatype"] == "PRCP":
                working_date_data[1] = results[j]["value"]
            elif results[j]["datatype"] == "TMAX":
                working_date_data[2] = results[j]["value"]
            elif results[j]["datatype"] == "TMIN":
                working_date_data[3] = results[j]["value"]

        # Add dict of results to date in the weather_data object
        weather_data[working_date].append(working_date_data)

    return weather_data
    
def main():
    """Output data for each station to its own JSON file"""
    # Dictionaries for JSON export
    station_data_object = dict()
    weather_data_object = dict()

    # Collect and add info to stations_info, weather_data
    for station in stations:
        # Add to stations_info
        print(f"Retrieving info for {station}")
        station_data_object[station] = retrieve_station_data(station, stations[station])

        # Add to weather_data
        print(f"Retrieving weather data for {station}")
        weather_data_object = retrieve_weather_data(station, stations[station], weather_data_object)

    # Write station info JSON to file
    with open("stations_info.json", "w") as station_output:
        json.dump(station_data_object, station_output)

    # Write station info JSON to file
    with open("weather_data.json", "w") as weather_output:
        json.dump(weather_data_object, weather_output)

if __name__ == "__main__":
    main()
