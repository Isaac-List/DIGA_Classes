import requests, json, noaa_token

# NOAA API token
token = noaa_token.token

# Station data endpoint
data_endpoint = "https://www.ncei.noaa.gov/cdo-web/api/v2/stations"

def get_stations_zip(zips: list) -> dict:
    """Get a list of stations that meet requirements"""
    # Return object
    stations = dict()

    # Update parameters
    for z in zips:
        # Parameters for weather data retrieval
        parameters = {
            "locationid": f"ZIP:{z}",
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

        # Select results with > 95% data coverage
        for i in range(len(station_results)):
            if float(station_results[i]["datacoverage"]) >= 0.95:
                stations[station_results[i]["name"]] = station_results[i]["id"]

    # Return results
    return stations

def get_stations_fips(fips: str) -> dict:
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
    choice: str = input("Choose to search by ZIP codes (1) or FIPS number (2): ")

    if choice == "1":
        # From ZIP Codes
        zip_codes = []

        print("Enter a zip code to search, type STOP when done.")
        zip_code = input("ZIP code: ")
        while zip_code != "STOP":
            zip_codes.append(zip_code)
            zip_code = input("ZIP code: ")

        station_ids_from_zip: dict = get_stations_zip(zip_codes)

        with open("station_ids_from_zip.json", "w") as output:
            json.dump(station_ids_from_zip, output)

    # From FIPS code
    elif choice == "2":
        fips = input("Enter your state's FIPS code: ")
        station_ids_from_fips: dict = get_stations_fips(fips)

        with open("station_ids_from_fips.json", "w") as output:
            json.dump(station_ids_from_fips, output)

    else:
        print("Invalid choice selection.")

if __name__ == "__main__":
    main()
