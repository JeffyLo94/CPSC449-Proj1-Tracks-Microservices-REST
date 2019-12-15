
curl -X POST http://localhost:8001/upstreams \
    --data "name=playAPI"

curl -X POST http://localhost:8001/upstreams/playAPI/targets \
    --data "target=localhost:5200" \
    --data "weight=6"

curl -X POST http://localhost:8001/upstreams/playAPI/targets \
    --data "target=localhost:5201" \
    --data "weight=6"

curl -X POST http://localhost:8001/upstreams/playAPI/targets \
    --data "target=localhost:5202" \
    --data "weight=6"

curl -X POST http://localhost:8001/services/ \
    --data "name=playlists" \
    --data 'host=playAPI'
    #--data "path=/tracksAPI"

curl -X POST http://localhost:8001/services/playlists/routes/ \
    --data 'name=playRoute' \
    --data 'paths[]=/playlists'
