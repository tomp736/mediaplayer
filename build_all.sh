#!/bin/bash

# Absolute path to this script. /home/user/bin/foo.sh
SCRIPT=$(readlink -f $0)
# Absolute path this script is in. /home/user/bin
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH

docker build . -f src/pymp_frontend/dockerfile -t pymp_frontend
docker build . -f src/pymp_frontend_api/dockerfile -t pymp_frontend_api
docker build . -f src/pymp_ffmpeg_svc/dockerfile -t pymp_ffmpeg_svc
docker build . -f src/pymp_media_svc/dockerfile -t pymp_media_svc
docker build . -f src/pymp_file_svc/dockerfile -t pymp_file_svc