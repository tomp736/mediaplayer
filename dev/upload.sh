#!/bin/bash

for file in *; do
    echo $file
    if [ -f "$file" ]; then
        curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@$file" localhost:8087/upload
    fi
done
