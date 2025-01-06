import requests
import csv
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

# Fetch metadata
meta_url = "https://heatpumpmonitor.org/system/list/public.json"
meta_response = requests.get(meta_url)
meta = meta_response.json()

# Fetch stats
stats_url = "https://heatpumpmonitor.org/system/stats/all"
stats_response = requests.get(stats_url)
stats = stats_response.json()

# Initialize geolocator
geolocator = Nominatim(user_agent="heatpumpmap", timeout=10)

def geocode_location(location):
    try:
        return geolocator.geocode(location)
    except (GeocoderTimedOut, GeocoderUnavailable):
        return None

def read_cached_locations(csv_file):
    cached_locations = {}
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cached_locations[row['location']] = (float(row['latitude']), float(row['longitude']))
    except FileNotFoundError:
        pass
    return cached_locations

def write_cached_locations(csv_file, cached_locations):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['location', 'latitude', 'longitude'])
        writer.writeheader()
        for location, coords in cached_locations.items():
            writer.writerow({'location': location, 'latitude': coords[0], 'longitude': coords[1]})

# Combine metadata and stats
systems = []
cached_locations = read_cached_locations('cached_locations.csv')

for system in meta:
    system_id = str(system['id'])
    if system_id in stats:
        system['stats'] = stats[system_id]

        # Check cached locations first
        location_str = system['location']
        if location_str in cached_locations:
            system['latitude'], system['longitude'] = cached_locations[location_str]
            print(f"Using cached coordinates for system ID {system_id}: ({system['latitude']}, {system['longitude']})")
        else:
            # Geocode location with retry logic
            location = None
            print(f"Geocoding location for system ID {system_id}: {location_str}")
            for attempt in range(1):  # Retry up to 3 times
                location = geocode_location(location_str)
                if location:
                    print(f"Geocoding successful for system ID {system_id} on attempt {attempt + 1}")
                    break
                print(f"Geocoding attempt {attempt + 1} failed for system ID {system_id}. Retrying...")
                time.sleep(1)  # Wait for 1 second before retrying

            if location:
                system['latitude'] = location.latitude
                system['longitude'] = location.longitude
                cached_locations[location_str] = (location.latitude, location.longitude)
                print(f"Geocoded coordinates for system ID {system_id}: ({location.latitude}, {location.longitude})")
            else:
                system['latitude'] = None
                system['longitude'] = None
                print(f"Geocoding failed for system ID {system_id}. Setting coordinates to None.")

        # Add system to the list
        systems.append(system)

# Write updated cached locations to CSV
write_cached_locations('cached_locations.csv', cached_locations)

# Print systems data for debugging
for system in systems:
    print("System data:", system)