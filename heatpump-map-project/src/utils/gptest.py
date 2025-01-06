from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="heatpumpmap")
location = geolocator.geocode("Newport")
print(location.latitude, location.longitude)


