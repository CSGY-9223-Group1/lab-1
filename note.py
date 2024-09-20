import json

class Note:
    def __init__(self, id, owner_id, note):
        self.id = id
        self.owner_id = owner_id
        self.note = note
        
    def set_note(self, note):
        self.note = note
        
