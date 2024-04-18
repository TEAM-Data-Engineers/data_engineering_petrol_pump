import osmnx as ox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

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