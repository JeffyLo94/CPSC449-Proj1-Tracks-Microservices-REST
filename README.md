# CPSC449-Proj1-Tracks-Microservices-REST
Project 1 for CPSC 449 w/ Prof Avery - Microservices with RESTful APIs

## Team Members:
### PART 1 Positions
* Ops  - Jeffrey Lo
* Dev1 - Oscar Cheung
* Dev2 - Mircea Dumitrache
### PART 2 Positions
* Ops - Mircea Dumitrache
* Dev1 - Oscar Cheung
* Dev2  - Jeffrey Lo

## PART 1 Responsibilities:
* Ops   owns the Procfile, REST population script, team management, and Tuffix deployment.
* Dev1  owns the Tracks and Playlists microservices.
* Dev2  owns the Users and Descriptions microservices.

## PART 2 Responsabilities:
* Ops   owns the loadbalancer (Kong), the minIO server, kong configuration shell scripts, and Tuffix deployment.
* Dev1  owns the three tracks databases and the tracks microservice with sharding
* Dev2  owns the xspf module and the xspf microservice 

## Requirements & Dependencies:
* Python 3.6.7
* Flask API
* PugSQL
* Foreman
* Tavern
* Pytest
* KONG
* MinIO
* requests
* memcached && pymemcached


## Tested on:
* Tuffix

# Configuration:
* Test script ports and host: ```tests/includes.yaml```
* Database url: ``` api.cfg ```
* Environment variables: ``` .env ```

* Shell scripts: kong_config_scrits/

# Running: 
* Initialize DB: ```foreman run initDB```
* Start micro-services: ```foreman start -m all=1,initDB=0 -e .env```
* Run Test Script: ```py.test --tb=short```

# Running using load balancer:
* In a new terminal run the following: '''sudo ulimit -n 4096 & kong start'''
* In a new terminal run the following: '''sudo ./minio server /data'''
* Run kong configuration files:
  * '''cd kong_config_scripts'''
  * '''./all.sh'''
  * NOTE: configuration can be cleared with: '''./clearAll.sh'''
* Initialize DB: '''foreman run initDB'''
* Start micro-services: '''foreman start -m all=3,initDB=0,XSPF=1 -e .env'''
* Optional Test Script: '''py.test --tb=short''' 
* Open a web browser and go to '''localhost:8000'''
  * Address Example: '''localhost:8000/media/Nocturne20.mp3''' or alternatively, replace the 'Nocturne20.mp3' with preffered media file
  * Address Example: '''localhost:8000/playlists/playlists/all'''

# Change Log:
## Milestone 1 - "Project 1"
* Tracks, Playlists, Users, Descriptions Microservices Established with PugSQL and Flask-API
* Test scripts for api - failing most tests
## Milestone 2 - "Project 2"
* Tracks DB sharding support w/ GUIDs
* Fixed Microservice APIS
* Test Scripts for APIs - passing all
* Added XSPF playlist microservice
* Kong API gateway added
* Min.io static files added for tracks

# Microservice APIs:
## Tracks
| Method | Route         | Description                                                                                       |
|---------|---------------|---------------------------------------------------------------------------------------------------|
| POST    | /tracks       | Create new track                                                                                  |
| GET     | /tracks       | Get all tracks                                                                                    |
| GET     | /tracks?query | Get first track that satisfies query parameters ex) /tracks?title=Canon%20in%20D&artist=Pachelbel |
| PUT     | /tracks?query | Edit the first track that matches query parameters                                                |
| Delete  | /tracks       | Delete all tracks                                                                                 |
| Delete  | /tracks?query | Delete first track that matches query parameters                                                  |

## Playlists
| Method | Route            | Description                                             |
|--------|------------------|---------------------------------------------------------|
| POST   | /playlists       | Create new playlist                                     |
| GET    | /playlists       | Get all playlists                                       |
| GET    | /playlists/#     | Get playlist matching # (row num or UUID - TBD)         |
| GET    | /playlists?query | Get the first playlist that satisfies query parameters  |
| PUT    | /playlists?query | Edit the first playlist that matches query parameters   |
| DELETE | /playlists       | Delete all playlists                                    |
| DELETE | /playlists/#     | Delete playlist that matches #                          |
| DELETE | /playlists?query | Delete the first playlist that matches query parameters |

* #### Request Body:
    ```json
    {
        "title": "personal songs",
        "creator": "user1",
        "description": "test",
        "urls": ["somesongURL"]
    }
    ```

## Users
| Method | Route        | Description                                                             |
|--------|--------------|-------------------------------------------------------------------------|
| POST   | /user        | Create new user, automatically hash the password when create user       |
| GET    | /user/?query | Get first user profile that matches query param, except hashed password |
| GET    | /user/#      | Get user that matches #, excluding hashed pass                          |
| GET    | /user?query  | Get first user that satisfies query parameters                          |
| PUT    | /user?query  | Edit the first user that matches query parameters with JSON provided    |
| PUT    | /user/#      | Edit user that matches #                                                |
| DELETE | /user/#      | Delete user that matches #                                              |
| DELETE | /user?query  | Delete the first user that matches query parameters                     |
| POST   | /user/auth   | Authenticates user w/ supplied username, password                       |

## Descriptions
| Method | Route              | Description                                        |
|--------|--------------------|----------------------------------------------------|
| POST   | /desc       | Create new description                             |
| GET    | /desc/#     | Get the description that matches #                 |
| GET    | /desc?query | Get the first description that matches query param |
