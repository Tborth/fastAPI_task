
#!/bin/bash
xhost +local:root

echo "Stopping configAPIs ..."
docker-compose down
docker-compose up -d --build 

echo "http://localhost:8001/docs"

