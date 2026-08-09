import requests, json, noaa_token

# NOAA API token
token = noaa_token.token

# Station data endpoint
data_endpoint = "https://www.ncei.noaa.gov/cdo-web/api/v2/stations"

def get_stations(fips: str) -> dict:
    """Get a list of stations that meet requirements"""
    # Return object
    stations = dict()

    # Parameters for weather data retrieval
    parameters = {
        "locationid": f"FIPS:{fips}",
        "sortfield": "name",
        "sortorder": "asc",
        "startdate": "2026-01-01",
        "enddate": "2026-03-31",
        "datatypeid": ["PRCP", "TMAX", "TMIN"],
        "limit": "1000"
    }

    # Request
    station_data = requests.get(data_endpoint, params = parameters, headers = token)

    # Look at results
    station_json = station_data.json()
    station_results = station_json.get("results", [])

    # Select results with >= 99% data coverage
    for i in range(len(station_results)):
        if float(station_results[i]["datacoverage"]) >= 0.999:
            stations[station_results[i]["name"]] = station_results[i]["id"]

    # Return results
    return stations

def main():
    fips = input("Enter your state's FIPS code: ")
    
    station_ids: dict = get_stations(fips)

    with open("station_ids.json", "w") as output:
        json.dump(station_ids, output)    

if __name__ == "__main__":
    main()
