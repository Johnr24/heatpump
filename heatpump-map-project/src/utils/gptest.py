from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="heatpumpmap")
location = geolocator.geocode("Ramsey,UK")
print(location.latitude, location.longitude)


