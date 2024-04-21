import osmnx as ox
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import geopandas as gpd


conn_string = 'postgresql://postgres:postgres@172.17.0.1:5434/stg_db'
db = create_engine(conn_string)
conn = db.connect()

city = "Christchurch, New Zealand"

tags = {'amenity':'fuel'}
amenities =  ox.features.features_from_place(query=city, tags=tags)
print(amenities)
amenities['Timestamp'] = pd.Timestamp.now()
gdf_amenities = gpd.GeoDataFrame(amenities, geometry='geometry')
gdf_amenities.to_postgis('pump_locations', con=db, if_exists='replace', index=True)
print('Petrol Pump Succesfully Created')

######

all_address =  ox.features.features_from_place(query=city)
all_address['Timestamp'] = pd.Timestamp.now()
gdf_all_address = gpd.GeoDataFrame(all_address, geometry='geometry')
gdf_all_address.to_postgis('all_address', con=db, if_exists='replace', index=True)
print('All Addresses Succesfully Created')


conn.commit()
conn.close()