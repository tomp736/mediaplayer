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


## Run:

``` sh
cd examples/basic
docker-compose up -d
```
Running docker-compose files included - you can expect the services to be bound to ports as follows.
- frontend: localhost:8080
- frontend-api: localhost:8081, *localhost:8082*, *localhost:8083*
- fileupload: localhost:8087
- prometheus: *localhost:9090*
- locust: *localhost:8089*

Prometheus and locust services are only included in '_metrics' example.
 
Frontend-api is only created on 8081 for basic.

## Upload:

``` sh
for file in *; do
    echo $file
    if [ -f "$file" ]; then
        curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@$file" localhost:8087/upload
    fi
done
```
