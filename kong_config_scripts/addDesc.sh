
curl -X POST http://localhost:8001/upstreams \
    --data "name=descAPI"

curl -X POST http://localhost:8001/upstreams/descAPI/targets \
    --data "target=localhost:5400" \
    --data "weight=6"

curl -X POST http://localhost:8001/upstreams/descAPI/targets \
    --data "target=localhost:5401" \
    --data "weight=6"

curl -X POST http://localhost:8001/upstreams/descAPI/targets \
    --data "target=localhost:5402" \
    --data "weight=6"

curl -X POST http://localhost:8001/services/ \
    --data "name=descriptions" \
    --data 'host=descAPI'
    #--data "path=/tracksAPI"

curl -X POST http://localhost:8001/services/descriptions/routes/ \
    --data 'name=descRoute' \
    --data 'paths[]=/descriptions'
