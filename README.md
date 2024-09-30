[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Lab 1 paste bin


## Available Endpoints

| Action | Endpoint | HTTP Method | Header| Body | Result |
|--------|----------|-------------|-------|------|--------|
| Register user | `/register` | `POST` | | (JSON): `{"id": <User_Email>, "name": <User_Name>}` | On successful registration (`HTTP 200`), will return user object with a JWT token. JWT token is generated based on only email ID locally.|
| Add Note | `/add_note` | `GET` | `token`: JWT token obtained during registration | (JSON): `{"note": <note body>, "is_public": <boolean set to true if note is public>}` | Note object after successful posting. Here, JWT token will be validated. |
| Home page | `/` | `GET` | | | All the public notes (`HTTP 200`)|
| Get all notes | `/get_all_notes` | `GET` | `token`: JWT token obtained during registration | | All public listed notes + user's private notes (`HTTP 200`). Here, JWT token will be validated.
| Update a note | `/update_note` | `POST`| `token`: JWT token obtained during registration | (JSON) `{"note_id": <ID_of_note_of_interest>, "note": <body of udpate note>}`| `HTTP 200`. Here, JWT token will be validated.
| Delete a note | `/delete_note` | `POST`| `token`: JWT token obtained during registration | (JSON) `{"note_id": <ID_of_note_of_interest>`}| `HTTP 200`. Here, JWT token will be validated.

## Usage

### Setting Up the Appication
Build docker image: `docker build --tag pastebin-docker-group1 .` (Note the period at the end of the command)

### Running the Application
Run docker image as container: `docker run -p 5001:5000 pastebin-docker-group1`

Please, note that currently the app doesn't use persistent storage. This means that when the app is shut down, information about users and notes will be lost.




