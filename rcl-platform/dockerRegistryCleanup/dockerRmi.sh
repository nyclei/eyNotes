docker rmi $(docker images -q -f dangling=true)
sleep 3
docker rm $(docker ps -a -f status=exited -q)
sleep 3
docker volume rm $(docker volume ls -f dangling=true -q)
