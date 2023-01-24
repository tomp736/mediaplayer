#!/bin/bash

# Absolute path to this script. /home/user/bin/foo.sh
SCRIPT=$(readlink -f $0)
# Absolute path this script is in. /home/user/bin
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH

docker build .. -f dockerfile.pymp_common -t pymp_common

docker build .. -f dockerfile.pymp_frontend -t pymp_frontend
docker build .. -f dockerfile.pymp_server -t pymp_server
docker build .. -f dockerfile.file_svc -t pymp_file_svc

docker build .. -f dockerfile.pymp_locust -t pymp_locust