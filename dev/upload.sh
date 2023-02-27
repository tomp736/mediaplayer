#!/bin/bash

mkdir done
for file in *; do
    echo $file
    if [ -f "$file" ]; then
        curl -X POST -F "file=@$file" http://api.pymp.labrats.work/media
        mv "$file" done
    fi
done
