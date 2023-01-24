# PYMP - Python Media Player

DIWHY Media Player  - A microservice experiment.

- App written in Python, using Flask.
- Observability provided by prometheus.
- Load tests provided by locust.

---

## Build:

``` sh
cd dev
./build-all.sh
sudo mkdir -p /srv/media/videos
sudo mkdir -p /srv/media/redis
sudo chown -R $USER:docker /srv/media
```


## Basic Example:

``` sh
cd examples/basic
docker-compose up -d
```
Running docker-compose files included in the basic example:
- frontend: localhost:8080
- server: localhost:8081

## Microservice Example:

``` sh
cd examples/multiple_frontend
docker-compose up -d
```
Running docker-compose files included in the multiple_frontend example:
- frontend: localhost:8080
- media-api: localhost:8081
- meta-api: localhost:8082
- thumb-api: localhost:8083
- media-svc: internal
- ffmpeg-svc: internal

Prometheus and locust services are only included in '_metrics' example.

- prometheus: localhost:9090
- locust: localhost:8089
 
## Upload:

``` sh
for file in *; do
    echo $file
    if [ -f "$file" ]; then
        curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@$file" localhost:8087/upload
    fi
done
```
