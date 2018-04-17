docker rmi --force awssandbox.registry.rccl.com/janitor:2.2.1
docker tag 4b32944db787 awssandbox.registry.rccl.com/janitor:2.2.1
docker push awssandbox.registry.rccl.com/janitor:2.2.1

docker rmi  --force awssandbox.registry.rccl.com/janitor:1.12.1
docker tag 4b32944db787 awssandbox.registry.rccl.com/janitor:1.12.1
docker push awssandbox.registry.rccl.com/janitor:1.12.1

docker rmi --force awssandbox.registry.rccl.com/janitor:2.1.2.1
docker tag 4b32944db787 awssandbox.registry.rccl.com/janitor:2.1.2.1
docker push awssandbox.registry.rccl.com/janitor:2.1.2.1

docker rmi --force awssandbox.registry.rccl.com/kafka-client:3.0.0
docker tag cb7b29c9e63c awssandbox.registry.rccl.com/kafka-client:3.0.0
docker push awssandbox.registry.rccl.com/kafka-client:3.0.0

docker rmi --force awssandbox.registry.rccl.com/kafka-client:3.5.0
docker tag cb7b29c9e63c awssandbox.registry.rccl.com/kafka-client:3.5.0
docker push awssandbox.registry.rccl.com/kafka-client:3.5.0

docker rmi --force awssandbox.registry.rccl.com/kafka-client:3.12.0
docker tag cb7b29c9e63c awssandbox.registry.rccl.com/kafka-client:3.12.0
docker push awssandbox.registry.rccl.com/kafka-client:3.12.0
