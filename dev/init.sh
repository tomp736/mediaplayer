#!/bin/bash

# Absolute path to this script. /home/user/bin/foo.sh
SCRIPT=$(readlink -f $0)
# Absolute path this script is in. /home/user/bin
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH

sudo mkdir -p /srv/media/videos
sudo mkdir -p /srv/media/index
sudo mkdir -p /srv/media/redis
sudo chown -R $USER:docker /srv/medias