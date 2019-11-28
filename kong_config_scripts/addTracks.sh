
curl -X POST http://localhost:8001/upstreams \
    --data "name=trackAPI"

curl -X POST http://localhost:8001/upstreams/trackAPI/targets \
    --data 'name=trackOne' \
    --data "target=localhost:6100" \
    --data "weight=100"

curl -X POST http://localhost:8001/upstreams/trackAPI/targets \
    --data 'name=trackTwo' \
    --data "target=localhost:6101" \
    --data "weight=100"

curl -X POST http://localhost:8001/upstreams/trackAPI/targets \
    --data 'name=trackThree' \
    --data "target=localhost:6102" \
    --data "weight=100"

curl -X POST http://localhost:8001/services/ \
    --data "name=tracks" \
    --data 'host=trackAPI'
    #--data "path=/track"

curl -X POST http://localhost:8001/services/track/routes/ \
    --data 'name=trackRoute' \
    --data 'paths[]=/tracksAPI'
