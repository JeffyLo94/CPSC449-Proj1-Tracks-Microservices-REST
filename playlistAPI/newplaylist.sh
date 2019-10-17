#!/bin/sh

curl --verbose \
     --request POST \
     --header 'Content-Type: application/json' \
     --data @newplaylist.json \
    http://localhost:5000/playlists

