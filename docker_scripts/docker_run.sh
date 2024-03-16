cd /media/sf_data_engineering/group_project/data_engineering_petrol_pump/docker_scripts
docker-compose -f docker-compose-petrol-pump.yaml up 
docker-compose -f docker-compose-petrol-pump.yaml down --remove orphans
#timeout 120 bash -c 'sleep 120 && kill -s SIGINT $$'
