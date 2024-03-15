import osmnx as ox
import psycopg2
import pandas as pd
from sqlalchemy import create_engine


city = "Christchurch, New Zealand"
tags = {'amenity':'fuel'}
amenities =  ox.features.features_from_place(query=city, tags=tags)
print(amenities)


# establish connections
conn_string = 'postgresql://postgres:postgres@172.17.0.1:5433/stg_db'

db = create_engine(conn_string)
conn = db.connect()
conn1 = psycopg2.connect(
    database="stg_db",
  user='postgres',
  password='postgres',
  host='172.17.0.1',
 port= '5433'
)

conn1.autocommit = True
cursor = conn1.cursor()

cursor.execute('drop table if exists public.airlines_final')

sql = '''CREATE TABLE public.airlines_final(id int ,
day int ,airline char(20),destination char(20));'''

cursor.execute(sql)

column_list = ['amenity','brand']
#engine = create_engine('postgresql://username:password@hostname:port/database_name')
amenities[column_list].to_sql('pump_locations', con=db, if_exists='replace', index=False)

print('Petrol Pump Succesfully Created')

conn1.commit()
conn1.close()

conn.commit()
conn.close()

