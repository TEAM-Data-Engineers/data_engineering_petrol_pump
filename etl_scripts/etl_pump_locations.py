import osmnx as ox


city = "Christchurch, New Zealand"
tags = {'amenity':'fuel'}
amenities =  ox.features.features_from_place(query=city, tags=tags)
print(amenities)
