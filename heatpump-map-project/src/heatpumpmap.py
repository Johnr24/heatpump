import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

# Range of system IDs to process
system_id_range = range(1, 50)

# Initialize geolocator
geolocator = Nominatim(user_agent="heatpumpmap", timeout=10)

def geocode_location(location):
    try:
        return geolocator.geocode(location)
    except (GeocoderTimedOut, GeocoderUnavailable):
        return None

systems = []

for system_id in system_id_range:
    try:
        # Fetch single system data
        system_url = f"https://heatpumpmonitor.org/system/get.json?id={system_id}"
        system_response = requests.get(system_url)
        system = system_response.json()

        # Fetch system stats
        stats_url = f"https://heatpumpmonitor.org/system/stats/all?id={system_id}"
        stats_response = requests.get(stats_url)
        stats = stats_response.json()

        # Merge stats into system data
        system['stats'] = stats[str(system_id)]

        # Geocode location 
        location = None
        location = geocode_location(system['location'])

        if location:
            system['latitude'] = location.latitude
            system['longitude'] = location.longitude
        else:
            system['latitude'] = None
            system['longitude'] = None

        # Add system to the list
        systems.append(system)
    except Exception as e:
        print(f"Skipping system ID {system_id} due to error: {e}")

# Print systems data for debugging
for system in systems:
    print("System data:", system)