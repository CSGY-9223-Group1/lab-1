import json


class User:
    def __init__(self, userid, name, token):
        self.userid = userid
        self.name = name
        self.token = token

    def get_userid(self):
        return self.userid

    def get_name(self):
        return self.name

    def get_token(self):
        return self.token

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
