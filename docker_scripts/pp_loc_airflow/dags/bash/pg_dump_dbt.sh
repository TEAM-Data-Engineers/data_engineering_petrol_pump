pg_dump --dbname='postgresql://postgres:postgres@172.17.0.1:5434/stg_db' --file=/home/hravat/airflow/dags/sql/pp_pg_restore.sql --schema=public_dbt_test__audit --inserts --clean

sed -i 's/postgres/hravat/g' /home/hravat/airflow/dags/sql/pp_pg_restore.sql
