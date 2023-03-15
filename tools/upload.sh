#!/bin/bash

# url=http://api.pymp.labrats.work/media
url=http://localhost:8081/media

mkdir done
for file in *; do
    echo $file
    if [ -f "$file" ]; then
        curl -X POST -F "file=@$file" $url
        mv "$file" done
    fi
done
