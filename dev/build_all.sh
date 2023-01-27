#!/bin/bash

# Absolute path to this script. /home/user/bin/foo.sh
SCRIPT=$(readlink -f $0)
# Absolute path this script is in. /home/user/bin
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH

docker build .. -f dockerfile.pymp_common -t ghcr.io/tomp736/pymp/pymp_common:latest-dev

docker build .. -f dockerfile.pymp_frontend -t ghcr.io/tomp736/pymp/pymp_frontend:latest-dev
docker build .. -f dockerfile.pymp_server -t ghcr.io/tomp736/pymp/pymp_server:latest-dev
docker build .. -f dockerfile.file_svc -t ghcr.io/tomp736/pymp/pymp_file_svc:latest-dev

docker build .. -f dockerfile.pymp_locust -t ghcr.io/tomp736/pymp/pymp_locust:latest-dev