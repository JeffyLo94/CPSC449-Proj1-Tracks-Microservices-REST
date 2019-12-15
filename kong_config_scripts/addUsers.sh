
curl -X POST http://localhost:8001/upstreams \
    --data "name=userAPI"

curl -X POST http://localhost:8001/upstreams/userAPI/targets \
    --data "target=localhost:5300" \
    --data "weight=6"

curl -X POST http://localhost:8001/upstreams/userAPI/targets \
    --data "target=localhost:5301" \
    --data "weight=6"

curl -X POST http://localhost:8001/upstreams/userAPI/targets \
    --data "target=localhost:5302" \
    --data "weight=6"

curl -X POST http://localhost:8001/services/ \
    --data "name=users" \
    --data 'host=userAPI'
    #--data "path=/tracksAPI"

curl -X POST http://localhost:8001/services/users/routes/ \
    --data 'name=userRoute' \
    --data 'paths[]=/users'
