#!/bin/bash

# Absolute path to this script. /home/user/bin/foo.sh
SCRIPT=$(readlink -f $0)
# Absolute path this script is in. /home/user/bin
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH

docker build .. -f dockerfile.common -t pymp_common

docker build .. -f dockerfile.frontend -t pymp_frontend
docker build .. -f dockerfile.frontend_api -t pymp_frontend_api
docker build .. -f dockerfile.ffmpeg_svc -t pymp_ffmpeg_svc
docker build .. -f dockerfile.media_svc -t pymp_media_svc
docker build .. -f dockerfile.file_svc -t pymp_file_svc
docker build .. -f dockerfile.locust -t pymp_locust