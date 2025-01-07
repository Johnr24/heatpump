import folium
from heatpumpmap import systems  # Assuming systems is a list of dictionaries with heat pump data
import matplotlib.colors as mcolors

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
        if 'latitude' in system and 'longitude' in system and system['latitude'] is not None and system['longitude'] is not None and 'running_cop' in system['stats']:
            latitude = system['latitude']
            longitude = system['longitude']
            cop = system['stats']['running_cop']
            if cop is not None:
                print(f"Latitude: {latitude}, Longitude: {longitude}, COP: {cop}")  # Print the geolocation and COP
                
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
                    <strong>ID:</strong> <a href="https://heatpumpmonitor.org/system/view?id={system['id']}" target="_blank">{system['id']}</a><br>
                    <strong>Model:</strong> {system['hp_model']}<br>
                    <strong>COP:</strong> {cop:.2f}
                </div>
                """
                
                folium.Marker(
                    location=[latitude, longitude],
                    icon=icon,
                    popup=folium.Popup(popup_html, max_width=300)
                ).add_to(heatmap)
            else:
                print(f"Skipping system ID {system['id']} due to missing COP.")
        else:
            print(f"Geolocation or COP data is missing for system ID {system['id']}.")

    # Add a custom control to toggle text labels
    toggle_js = """
    function toggleLabels() {
        var texts = document.getElementsByClassName('cop-text');
        for (var i = 0; i < texts.length; i++) {
            if (texts[i].style.display === 'none') {
                texts[i].style.display = 'inline';
            } else {
                texts[i].style.display = 'none';
            }
        }
    }
    """
    toggle_button = folium.Element('<button onclick="toggleLabels()">Toggle Labels</button>')
    heatmap.get_root().html.add_child(folium.Element(f'<script>{toggle_js}</script>'))
    heatmap.get_root().html.add_child(toggle_button)

    # Save the map to an HTML file
    heatmap.save('index.html')

if __name__ == "__main__":
    plot_heatpump_map(systems)