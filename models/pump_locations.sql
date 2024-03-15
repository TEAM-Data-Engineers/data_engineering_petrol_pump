-- films.sql
SELECT * FROM {{ source('stg_db', 'pump_locations') }}
