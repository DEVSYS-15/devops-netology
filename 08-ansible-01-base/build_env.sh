#!/bin/bash
set -e
DIMG='ubuntu centos7 fedora'
TAG=1.0.0
PRREFIX=netology
for i in $DIMG; do
    docker build -t $i:$TAG docker_build/$i/ 2>&1>/dev/null && \
    docker run --name $i-$PRREFIX  -it -d $i:$TAG  
done

ansible-playbook  -i playbook/inventory/prod.yml playbook/site.yml

for i in $DIMG; do
   echo -e $(docker kill  $i-$PRREFIX ) is stop
   echo -e $(docker rm -f $i-$PRREFIX ) is remove
done