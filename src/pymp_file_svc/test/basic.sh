#!/bin/bash

# Set the maximum number of iterations
max_iterations=100
host=localhost
port=8081

# Set the delay time in seconds
delay=1

# Use a for loop to execute the curl command 1000 times
for i in $(seq 1 $max_iterations); do
  dd if=/dev/random of=/tmp/upload-$i bs=1024 count=1024 status=none >/dev/null
  curl -s -X POST -F "file=@/tmp/upload-$i" http://$host:$port/upload | curl -s -X POST -H "Content-Type: application/json" -d @- http://$host:$port/download --output /tmp/download-$i
  ulsum=$(sha256sum /tmp/upload-$i | cut -d ' ' -f 1 | tr -d ' ')
  dlsum=$(sha256sum /tmp/download-$i | cut -d ' ' -f 1 | tr -d ' ')
  if [ "$ulsum" == "$dlsum" ]; then
    echo "$i Sums are equal"
  else
    echo "$i Sums are not equal"
  fi
  rm /tmp/download-$i
  rm /tmp/upload-$i
done
