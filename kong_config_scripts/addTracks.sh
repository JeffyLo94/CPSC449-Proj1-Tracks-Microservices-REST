
curl -X POST http://localhost:8001/upstreams \
    --data 'name=trackAPI'

curl -X POST http://localhost:8001/upstreams/trackAPI/targets \
    --data 'target=127.0.0.1:5100' \
    --data 'weight=6'

curl -X POST http://localhost:8001/upstreams/trackAPI/targets \
    --data 'target=127.0.0.1:5101' \
    --data 'weight=6'

curl -X POST http://localhost:8001/upstreams/trackAPI/targets \
    --data 'target=127.0.0.1:5102' \
    --data 'weight=6'

curl -X POST http://localhost:8001/services/ \
    --data 'name=tracksSer' \
    --data 'host=trackAPI' \
    --data "path=localhost"

curl -X POST http://localhost:8001/services/tracksSer/routes/ \
    --data 'name=trackRoute' \
    --data 'paths[]=/tracks'
