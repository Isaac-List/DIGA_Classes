"""
Isaac List
DIGA620 Summer 2026
Final Project
"""

import requests, json, noaa_token

# Stations used for prototype
stations = {
    "La Crosse": "GHCND:USC00474373",
    "Holmen": "GHCND:US1WILC0022",
    "West Salem": "GHCND:US1WILC0001",
    "Coon Valley": "GHCND:US1WILC0021",
    "Stoddard": "GHCND:US1WIVR0010",
    "Viroqua": "GHCND:US1WILC0021"
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
    """Retrieve data for given station and add to object"""
    # Build structure
    station_data = {
        "station_id": station_id,
        "station_name": station,
        "latitude": -999,
        "longitude": -999,
        "elevation": -999,
        "dates": {}
    }

    #
    # Get station information
    #

    # Update URL path
    url = "https://www.ncei.noaa.gov/cdo-web/api/v2/stations/" + station_id

    # Request
    station_info = requests.get(url, headers = token)

    # Fill in lat, lon, elev data
    station_data["latitude"] = station_info.json()["latitude"]
    station_data["longitude"] = station_info.json()["longitude"]
    station_data["elevation"] = station_info.json()["elevation"]

    #
    # Get station weather data
    #
    
    # Update stationid in parameters
    parameters["stationid"] = station_id

    # Request
    station_weather = requests.get(data_endpoint, params = parameters, headers = token)

    # Fill in precipitation, max temp, min temp for each of the dates (~90 days)
    results: list = station_weather.json()["results"]

    # Results are in sets of 3 -> Precipitation, TMAX, TMIN
    for i in range(0, len(results) - 2, 3):
        # Get 4 values from results: date will be key
        working_date = results[i]["date"]

        # These will be values
        working_date_data = dict()
        working_date_data["precip"] = results[i]["value"]
        working_date_data["max_temp"] = results[i + 1]["value"]
        working_date_data["min_temp"] = results[i + 2]["value"]

        # Add dict of results to station_data
        station_data["dates"][working_date] = working_date_data

    return station_data
    
def main():
    """Output data for each station to its own JSON file"""
    for station in stations:
        print(f"Retrieving data for {station}")
        station_data_object: dict = retrieve_station_data(station, stations[station])
        with open(f"{station}.json", "w") as output:
            json.dump(station_data_object, output)
        
if __name__ == "__main__":
    main()
