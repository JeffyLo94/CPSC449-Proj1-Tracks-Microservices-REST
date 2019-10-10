# CPSC449-Proj1-Tracks-Microservices-REST
Project 1 for CPSC 449 w/ Prof Avery - Microservices with RESTful APIs

## Team Members:
* Ops  - Jeffrey Lo
* Dev1 - Oscar Cheung
* Dev2 - Mircea Dumitrache


## Responsibilities:
* Ops   owns the Procfile, REST population script, team management, and Tuffix deployment.
* Dev1  owns the Tracks and Playlists microservices.
* Dev2  owns the Users and Descriptions microservices.

## Technologies:
* Python 3.6.7
* Flask API
* PugSQL
* Foreman

## Tested on:
* Tuffix

## Microservice APIs:

### Tracks
| Request | Route         | Description                                                                                       |
|---------|---------------|---------------------------------------------------------------------------------------------------|
| POST    | /tracks       | Create new track                                                                                  |
| GET     | /tracks       | Get all tracks                                                                                    |
| GET     | /tracks?query | Get first track that satisfies query parameters ex) /tracks?title=Canon%20in%20D&artist=Pachelbel |
| PUT     | /tracks?query | Edit the first track that matches query parameters                                                |
| Delete  | /tracks       | Delete all tracks                                                                                 |
| Delete  | /tracks?query | Delete first track that matches query parameters                                                  |

### Playlists
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

### Users


### Descriptions
