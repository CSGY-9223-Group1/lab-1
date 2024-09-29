# lab-1
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Lab 1 paste bin

Register user (/register)
Input - emailID (used as ID), name
Response - On successful registration will return user object with a JWT token (http 200)
JWT token is generated based on only email ID locally.

Add Note (/add_note)
Input - JWT token (http header "token"), note object - {note, is_public}
Response - Note object after successful posting
Here, jwt token will be validated

Home page (/)
Input - N/A
Response - Return all the Public notes (http 200)

Get all notes (/get_all_notes)
Input - JWT token (http header "token")
Response - All public listed notes + user's private notes (http 200)
Here, jwt token will be validated

Delete a note (/delete_note)
Input - JWT token (http header "token"), note object - {note_id}
Response - http 200
Here, jwt token will be validated

Build docker image - docker build --tag pastebin-docker-group1 . 
Run docker image as container - docker run -p 5001:5000 pastebin-docker-group1

App doesn't use Persistent storage. It uses dynamic memory. This means when App is shut down, Users, Notes will be lost