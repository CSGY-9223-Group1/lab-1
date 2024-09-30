[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Lab 1 paste bin
This is an internal Pastebin-like application that suports simple notes creation and management. At this point, it's primarily a JSON API-only application. Please, see available API endpoints information below.

## Available Endpoints

| Action | Endpoint | HTTP Method | Header| Body | Result |
|--------|----------|-------------|-------|------|--------|
| Register user | `/register` | `POST` | | (JSON): `{"id": <User_Email>, "name": <User_Name>}` | On successful registration (`HTTP 200`), will return user object with a JWT token. JWT token is generated based on only email ID locally.|
| Add Note | `/add_note` | `GET` | `token`: JWT token obtained during registration | (JSON): `{"note": <note body>, "is_public": <boolean set to true if note is public>}` | Note object after successful posting. Here, JWT token will be validated. |
| Home page | `/` | `GET` | | | All the public notes (`HTTP 200`)|
| Get all notes | `/get_all_notes` | `GET` | `token`: JWT token obtained during registration | | All public listed notes + user's private notes (`HTTP 200`). Here, JWT token will be validated.
| Update a note | `/update_note` | `POST`| `token`: JWT token obtained during registration | (JSON) `{"note_id": <ID_of_note_of_interest>, "note": <body of udpate note>}`| `HTTP 200`. Here, JWT token will be validated.
| Delete a note | `/delete_note` | `POST`| `token`: JWT token obtained during registration | (JSON) `{"note_id": <ID_of_note_of_interest>}`| `HTTP 200`. Here, JWT token will be validated.

## Usage

### Setting Up the Appication
The application requires secrets (e.g., JWT secret) and those need to be written to a `.env` file as key-value pairs following SECRET=VALUE convention. To make it easier to set up this file initially (i.e., pre-populate secret names/keys), simply save a copy of `.env.template` as `.env` like so:
```
cp -n .env.template .env
```
The `.env` file is listed in project's `.gitignore` file to prevent accidental disclosure of secrets in source code. Moreover, `.env` file is also listed in `.dockerignore` to prevent accidental copying of plaintext secret values into Docker image.

The application is set up to run as a Docker container. To build a Docker image necessary to run the application, run the follwoing:
```
docker build --tag pastebin-docker-group1 .
```


### Running the Application
Run Docker image as container:
```
docker run --env-file .env -p 5001:5000 pastebin-docker-group1
```

Upon successful launch of Docker command above, application will be listening to API calls on `localhost:5001`. 

Please, note that currently the app doesn't use persistent storage. This means that when the app is shut down, information about users and notes will be lost.