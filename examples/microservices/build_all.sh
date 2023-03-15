#!/bin/bash

# Absolute path to this script. /home/user/bin/foo.sh
SCRIPT=$(readlink -f $0)
# Absolute path this script is in. /home/user/bin
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH

docker build ../src -f ../src/pymp_frontend/dockerfile \
    -t pymp_frontend

docker build ../src -f ../src/pymp_core/dockerfile \
    -t pymp_core

docker build ../src -f ../src/pymp_server/dockerfile \
    -t pymp_server \
    --build-arg "BASE_IMAGE=pymp_core"

docker build ../src -f ../src/pymp_locust/dockerfile \
    -t pymp_locust