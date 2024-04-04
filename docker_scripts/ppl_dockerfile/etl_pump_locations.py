import osmnx as ox
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import geopandas as gpd

city = "Christchurch, New Zealand"
tags = {'amenity':'fuel'}
amenities =  ox.features.features_from_place(query=city, tags=tags)
print(amenities)


#drop_column_list = ['geometry','nodes']
#amenities = amenities.drop(columns=drop_column_list)
amenities['Timestamp'] = pd.Timestamp.now()
gdf_amenities = gpd.GeoDataFrame(amenities, geometry='geometry')

# establish connections
conn_string = 'postgresql://postgres:postgres@172.17.0.1:5434/stg_db'
db = create_engine(conn_string)
conn = db.connect()
#amenities.to_sql('pump_locations', con=db, if_exists='replace', index=True)
gdf_amenities.to_postgis('pump_locations', con=db, if_exists='replace', index=True)

print('Petrol Pump Succesfully Created')

conn.commit()
conn.close()