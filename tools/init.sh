#!/bin/bash

# Absolute path to this script. /home/user/bin/foo.sh
SCRIPT=$(readlink -f $0)
# Absolute path this script is in. /home/user/bin
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH

sudo mkdir -p /srv/pymp/media1/videos
sudo mkdir -p /srv/pymp/media1/index
sudo chown -R $USER:root /srv/media1

sudo mkdir -p /srv/pymp/redis
sudo chown -R $USER:root /srv/redis

sudo mkdir -p /srv/pymp/grafana
sudo chown -R $USER:root /srv/grafana

# NOBODY:NOGROUP
sudo mkdir -p /srv/pymp/prometheus
sudo chown 65534:65534 /srv/pymp/prometheus