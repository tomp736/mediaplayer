#!/bin/sh

cp ./templates/index.html ./index.html
cp ./templates/app.js ./app.js

sed -i "s|{{ media_host }}|$MEDIA_URL|g" app.js
sed -i "s|{{ meta_host }}|$META_URL|g" app.js
sed -i "s|{{ thumb_host }}|$THUMB_URL|g" app.js
busybox httpd -f -v -p 80