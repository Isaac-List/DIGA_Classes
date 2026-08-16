"""
Isaac List
DIGA620 Summer 2026
Final Project
"""

import json

def convert_to_geojson(input_json: dict) -> dict:
    """Convert from download_data output to GeoJSON"""
    # Create GeoJSON object
    result = {
        "type": "FeatureCollection",
        "features": []
    }

    # For each station, add to the features list
    # Include [long, lat, elev] for coordinates
    # Other info as properties dictionary
    for station in input_json:
        # For cleaner code
        data = input_json[station]
        
        # Coordinates
        long = data["Longitude"]
        lat = data["Latitude"]
        elev = data["Elevation"]

        # Properties
        station_id = data["Station_ID"]
        station_name = data["Station_Name"]
        zip_code = data["Zip"]
        county = data["County"]
        state = data["State"]

        # Put it together
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [long, lat, elev]
            },
            "properties": {
                "Station_ID": station_id,
                "Station_Name": station_name,
                "Zip": zip_code,
                "County": county,
                "State": state
            }
        }

        # Add to result
        result["features"].append(feature)

    return result

def main():
    with open("stations_info.json", "r") as source:
        source_json = json.load(source)
    converted_json = convert_to_geojson(source_json)

    with open("stations.geojson", "w") as output:
        json.dump(converted_json, output)

if __name__ == "__main__":
    main()
