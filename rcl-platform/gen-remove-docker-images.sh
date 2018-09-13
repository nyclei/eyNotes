#!/bin/bash

REGISTRY='tst2-registry.nowlab.tstsh.tstrccl.com'

if [ -z "$1" ]; then
    echo "Missing registry name"
    echo "   Usage: ./gen-remove-docker-images.sh 'tst2-registry.nowlab.tstsh.tstrccl.com'"
    exit 1
fi


OUTPUTFILE='/tmp/remove-docker-images.sh'
echo "#!/bin/bash" > $OUTPUTFILE
#docker images --format "docker rmi {{.Repository}}:{{.Tag}}" | grep -v 'master.mesos' | sed "s/$/ \&\&/g" | sort >> $OUTPUTFILE
docker images --format "docker rmi {{.Repository}}:{{.Tag}} 2> /dev/null " | grep $REGISTRY | sort >> $OUTPUTFILE
chmod a+x $OUTPUTFILE
echo 'docker images | wc -l' >>  $OUTPUTFILE
