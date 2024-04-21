import osmnx as ox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from geopy.distance import distance
import geopandas as gpd

def get_coordinates_from_address(address):
    location = ox.geocode(address)
    #osm_id = ox.utils_geo.get_nearest_node(ox.graph_from_point(location, dist=100), location)
    osm_id = 'temp placeholer'
    return location,osm_id

def get_petrol_pump_locations(address):
    
    conn_string = 'postgresql://hravat:hravat@localhost:5432/prod_de_db'
    engine = create_engine(conn_string)
    conn = engine.connect()
    
    table_name = 'prod_petrol_pump_locations.pump_locations'
    df = pd.read_sql_query(f'SELECT brand,name FROM {table_name} ORDER BY RANDOM() LIMIT 10', engine)
    
    conn.close()
    
    return df,'Connection Successful to DB'

def nearest_pp_distance(address):
    
    conn_string = 'postgresql://hravat:hravat@localhost:5432/prod_de_db'
    engine = create_engine(conn_string)
    conn = engine.connect()

    new_address = address.replace(" ", "%%")

    query = "SELECT * FROM prod_petrol_pump_locations.nearest_pumps_to_address where upper(address) like upper('"+new_address+"')"  # Use LIMIT 1 for efficiency
    print(query)    
    #query = "SELECT * FROM prod_petrol_pump_locations.nearest_pumps_to_address"
    gdf = pd.read_sql(query, engine) 
	
    if len(gdf) > 0:

        pass

    else:
        table_name = 'prod_petrol_pump_locations.pump_locations'
        gdf = gpd.read_postgis(f'SELECT brand,name,geometry as geom FROM {table_name}', engine)
        gdf['geom'] = gdf.geometry.centroid
    
        latitude,longitude = ox.geocode(address)
    
        def  dist_compute(latitude_1,longitude_1,row):
            #print(row.x)
            #print(row.y)
            return distance((latitude_1,longitude_1),(row.y,row.x))
    
        def extract_distance(geodesic_str):
            return round(float(geodesic_str.split()[0]),2)
    
        #gdf.set_crs(epsg=4326, inplace=True)
        gdf['distance'] = gdf['geom'].apply(lambda row: dist_compute(latitude,longitude,row))
        gdf = gdf.sort_values(by=['distance'])
        gdf = gdf.iloc[:10]
        gdf.reset_index(inplace=True)
        gdf.drop(columns=['geom','index'],inplace=True)
    
        gdf['address'] = address
        gdf['distance'] =  gdf['distance'].astype(str)
        gdf['distance'] = gdf['distance'].apply(extract_distance)
        gdf['distance'] = gdf['distance'].astype(float)
    
    
    
        gdf.to_sql( schema='prod_petrol_pump_locations', 
                    name='nearest_pumps_to_address', 
                    if_exists='append', 
                    index=False, 
                    con=engine)   
    conn.commit()
    conn.close()
    
    return gdf,'Connection Successful to DB'