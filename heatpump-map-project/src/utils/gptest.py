from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="heatpumpmap")
location = geolocator.geocode("Fairburn, Manchester ,UK")
print(location.latitude, location.longitude)


