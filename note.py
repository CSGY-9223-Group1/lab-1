import json


class Note:

    def __init__(self, note_id, owner_id, note, is_public):
        self.note_id = note_id
        self.owner_id = owner_id
        self.note = note
        self.is_public = is_public

    def get_note_id(self):
        return self.note_id

    def get_owner_id(self):
        return self.owner_id

    def get_note(self):
        return self.note

    def set_note(self, upd_note):
        self.note = upd_note

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
