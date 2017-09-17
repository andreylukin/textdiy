import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyAR2OXiT53hrsAgwl4Cm9BCy-6Yiv_uTI0')

# Geocoding an address
zipcode = 30313

# geocode_result = gmaps.geocode(zipcode)



# geocode_result[0]['geometry']['location']
# lat = geocode_result[0]['geometry']['location'].get('lat')
# lng = geocode_result[0]['geometry']['location'].get('lng')
# coord = (lat, lng)

result = gmaps.places("Home Depot " + str(zipcode))
address = result.get('results')[0].get('formatted_address')










		







