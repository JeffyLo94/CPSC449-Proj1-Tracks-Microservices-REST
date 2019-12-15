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

## Responsibilities:
* Ops   owns the Procfile, REST population script, team management, and Tuffix deployment.
* Dev1  owns the Tracks and Playlists microservices.
* Dev2  owns the Users and Descriptions microservices.

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


# Running: 
* Initialize DB: ```foreman run initDB```
* Start micro-services: ```foreman start -m all=1,initDB=0 -e .env```
* Run Test Script: ```py.test --tb=short``` 

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
