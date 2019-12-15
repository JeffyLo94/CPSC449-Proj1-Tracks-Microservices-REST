#!/bin/bash



service_ID=$(curl -X POST \
  --url http://localhost:8001/services/ \
  --data 'name=mediaMinIO' \
  --data 'url=http://localhost:9000/tracks' | jq --raw-output '.id')

curl -i -X POST \
  --url http://localhost:8001/services/mediaMinIO/routes \
  --data 'name=mediaRoute' \
  --data 'paths[]=/media' \
  --data 'service.id=${serviceID}'

#  --data 'hosts[]=localhost' \

#curl -i -X POST http://localhost:8001/routes/ \
#    -d 'name=mediaRouteAlt' \
#    -d 'hosts[]=minIO.com' \
#    -d 'paths[]=/media' \
#    -d 'service.id=${serviceID}'
