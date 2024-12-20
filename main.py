import json
import os
import sys
import traceback
import typing
from functools import wraps
from typing import cast

import jwt
from flask import Flask, jsonify, request

import note
import user

app = Flask(__name__)

users: typing.Dict[str, str] = {}
notes: typing.Dict[int, str] = {}
secret_key = os.environ.get("SECRET_KEY")


def token_required(f):
    def decorated(*args, **kwargs):
        token = None
        token_header = request.headers.get("token")
        if not token_header:
            return jsonify({"error": "token is missing"}), 403
        try:
            print("token - " + token_header)
            token = jwt.decode(token_header, secret_key, algorithms=["HS256"])
            print(json.dumps(token))
            current_user = users.get(token["user"])
            print("current user - " + json.dumps(current_user.__dict__))
        except Exception as ex:
            print("Exception")
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            return jsonify({"error": "token is invalid/expired"}), 403
        return f(current_user, *args, **kwargs)

    decorated.__name__ = f.__name__
    return decorated


@app.route("/")
def home():
    ret_list = []
    for key, value in notes.items():
        note_v = cast(note.Note, value)
        if note_v.is_public == True:
            ret_list.append(note_v)
    return jsonify([n.toJson() for n in ret_list])


@app.route("/register", methods=["POST"])
def register():
    content = request.json
    if content["id"] in users.keys():
        return jsonify('{"error": "ID already registered"}')
    jwt_data = {"user": content["id"]}

    encoded_jwt = jwt.encode(jwt_data, secret_key, algorithm="HS256")
    print("JWT generated - " + encoded_jwt)
    user1 = user.User(content["id"], content["name"], encoded_jwt)
    users[content["id"]] = user1

    return jsonify(user1.toJson())


@app.route("/add_note", methods=["POST"])
@token_required
def add_note(current_user):
    print("current user - " + json.dumps(current_user.__dict__))
    content = request.json
    print(content)
    input_note = content["note"]
    is_public = content["is_public"]
    note_object = note.Note(
        len(notes) + 1, str(current_user.get_userid()), str(input_note), is_public
    )
    notes[note_object.note_id] = note_object
    return jsonify(note_object.toJson())


@app.route("/get_all_notes", methods=["GET"])
@token_required
def get_all_notes(current_user):
    ret_list = []
    for key, value in notes.items():
        note_v = cast(note.Note, value)
        if note_v.is_public == True or current_user.get_userid() == note_v.owner_id:
            ret_list.append(note_v)
    json_string = json.dumps([n.toJson() for n in ret_list])
    return jsonify([n.toJson() for n in ret_list])


@app.route("/delete_note", methods=["POST"])
@token_required
def delete_note(current_user):
    content = request.json
    id_to_delete = content["note_id"]
    if notes.get(id_to_delete) is not None:
        note_v = cast(note.Note, notes.get(id_to_delete))
        if (
            note_v.note_id == id_to_delete
            and current_user.get_userid() == note_v.owner_id
        ):
            notes.pop(id_to_delete)
        else:
            return '{"status": "note not found"}'
    return jsonify('{"status": "success"}')


@app.route("/update_note", methods=["POST"])
@token_required
def update_note(current_user):
    content = request.json
    id_to_update = content["note_id"]
    if notes.get(id_to_update) is not None:
        note_v = cast(note.Note, notes.get(id_to_update))
        if (
            note_v.note_id == id_to_update
            and current_user.get_userid() == note_v.owner_id
        ):
            if "note" in content:
                note_new_content = content["note"]
                notes[id_to_update].set_note(note_new_content)
            if "is_public" in content:
                notes[id_to_update].is_public = content["is_public"]

        else:
            return '{"status": "note not found"}'
    return jsonify('{"status": "success"}')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
