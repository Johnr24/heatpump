import folium
from heatpumpmap import systems  # Assuming systems is a list of dictionaries with heat pump data

def plot_heatpump_map(systems):
    # Create a map centered around a central point
    map_center = [51.509865, -0.118092]  # Example: London coordinates
    heatmap = folium.Map(location=map_center, zoom_start=6)

    # Add markers for each system
    for system in systems:
        if 'latitude' in system and 'longitude' in system and 'running_cop' in system['stats']:
            latitude = system['latitude']
            longitude = system['longitude']
            cop = system['stats']['running_cop']
            if cop is not None:
                print(f"Latitude: {latitude}, Longitude: {longitude}, COP: {cop}")  # Print the geolocation and COP
                
                # Create a custom icon with the COP value
                icon = folium.DivIcon(
                    icon_size=(150, 36),
                    icon_anchor=(0, 0),
                    html=f'<div style="font-size: 12pt; color: blue;">{cop:.2f}</div>'
                )
                
                folium.Marker(
                    location=[latitude, longitude],
                    icon=icon,
                    popup=f"ID: {system['id']}<br>Model: {system['hp_model']}<br>COP: {cop:.2f}"
                ).add_to(heatmap)
            else:
                print(f"Skipping system ID {system['id']} due to missing COP.")
        else:
            print(f"Geolocation or COP data is missing for system ID {system['id']}.")

    # Save the map to an HTML file
    heatmap.save('heatpump_map.html')

if __name__ == "__main__":
    plot_heatpump_map(systems)