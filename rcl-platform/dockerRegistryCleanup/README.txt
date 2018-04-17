Steps to setup the cronjob for cleaning private docker registry on node 10.16.7.73 (AWSSandbox Docker Registry Node):
0) sudo su   # as 'root'
1) copy two executable python scripts to /usr/bin:
  - /home/mesossu/dockerRegistryCleanup/cleanup-docker-registry.py
  - /home/mesossu/dockerRegistryCleanup/delete_docker_registry_image.py
2) Run 'source /home/mesossu/dockerRegistryCleanup/setRegDataPath.sh' to set the environment varible "REGISTRY_DATA_DIR" (this is for current session only for directly testing 'cleanup-docker-registry.py')
3) Add the output from step 2 to root user .bashrc file for future root session.  (I didn't automate this step.)
4) Add following cronjob with either "crontab -e" manually, or using pipe way to append following to existing "crontab -l" :
> 30 * * * *      cleanup-docker-registry.py -n 2        > /dev/null 2>&1


How to verify?
1) You can go to following url to check the list of images in the registry:
  https://awssandbox.registry.rccl.com/v2/_catalog

2) Then you can check each image's tags-list here: 
  https://awssandbox.registry.rccl.com/v2/janitor/tags/list       (*)
  https://awssandbox.registry.rccl.com/v2/kafka-client/tags/list

On AWSSandbox docker registry, because the cron job was set up for every hour, running at every 30th minute,  you can come to above tags-list URLs before & after every 30th minutes of each hour.

Because the cronjob is set with "-n 2", which means we will perserve 2 latest versions (or say Tags) of each image and delete all other tags, any older version of image will be pruned. For your playing/testing, you can use following docker commands to add version to the registry 'Before', then check the registry 'After':

> docker rmi --force awssandbox.registry.rccl.com/janitor:1.0.1
> docker tag 4b32944db787 awssandbox.registry.rccl.com/janitor:1.0.1
> docker push awssandbox.registry.rccl.com/janitor:1.0.1
> docker rmi --force awssandbox.registry.rccl.com/janitor:1.0.1  #clean your local

By refreshing the tags-list url (*), you are expecting this version of 1.0.1 be pruned when there are 2 more newer versions of 'janitor' tags in registry already.

