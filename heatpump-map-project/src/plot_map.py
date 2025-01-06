import folium
from heatpumpmap import systems  # Assuming systems is a list of dictionaries with heat pump data
import matplotlib.colors as mcolors
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

# Initialize geolocator
geolocator = Nominatim(user_agent="heatpumpmap", timeout=10)

def geocode_location(location):
    try:
        return geolocator.geocode(location)
    except (GeocoderTimedOut, GeocoderUnavailable):
        return None

def get_color(cop, min_cop, max_cop):
    norm = mcolors.Normalize(vmin=min_cop, vmax=max_cop)
    cmap = mcolors.LinearSegmentedColormap.from_list("cop_cmap", ["red", "orange", "green"])
    return mcolors.to_hex(cmap(norm(cop)))

def plot_heatpump_map(systems):
    # Create a map centered around a central point
    map_center = [51.509865, -0.118092]  # Example: London coordinates
    heatmap = folium.Map(location=map_center, zoom_start=6)

    # Determine the range of COP values
    cop_values = [system['stats']['running_cop'] for system in systems if 'running_cop' in system['stats'] and system['stats']['running_cop'] is not None]
    min_cop = min(cop_values)
    max_cop = max(cop_values)

    # Add markers for each system
    for system in systems:
        if 'location' in system and 'running_cop' in system['stats']:
            location_str = system['location']
            cop = system['stats']['running_cop']
            if cop is not None:
                # Geocode the location
                location = None
                for attempt in range(3):  # Retry up to 3 times
                    location = geocode_location(location_str)
                    if location:
                        break
                    time.sleep(1)  # Wait for 1 second before retrying

                if location:
                    latitude = location.latitude
                    longitude = location.longitude
                    print(f"Location: {location_str}, Latitude: {latitude}, Longitude: {longitude}, COP: {cop}")  # Print the geolocation and COP

                    # Get color based on COP value
                    color = get_color(cop, min_cop, max_cop)

                    # Create a custom icon with the COP value on a black background with 50% transparency
                    icon = folium.DivIcon(
                        icon_size=(150, 36),
                        icon_anchor=(0, 0),
                        html=f'''
                        <div class="cop-label" style="font-size: 12pt; color: black; background-color: rgba(0, 0, 0, 0); padding: 2px; display: flex; align-items: center;">
                            <div style="width: 10px; height: 10px; background-color: {color}; border-radius: 50%; margin-right: 5px;"></div>
                            <span class="cop-text">{cop:.2f}</span>
                        </div>
                        '''
                    )

                    # Create a popup with a clickable link
                    popup_html = f"""
                    <div>
                        <a href="{system['url']}" target="_blank">View Details</a>
                    </div>
                    """
                    popup = folium.Popup(popup_html, max_width=300)

                    # Add marker to the map
                    folium.Marker(
                        location=[latitude, longitude],
                        icon=icon,
                        popup=popup
                    ).add_to(heatmap)

    # Save the map to an HTML file
    heatmap.save('heatpump_map.html')

# Call the function to plot the map
plot_heatpump_map(systems)