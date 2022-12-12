#DEV 
1. Listiong available containers `docker ps`
2. to enter container `docker exec -it {id} bash`
3. To rebuild container `docker-compose build {name}`
4. to start project's containers `docker-compose up`
5. To start containers without starting the server `docker compose -f 'docker-compose.yml'  -p 'capstone' start`