from flask import Flask
from flask import request
import note
import json

app = Flask(__name__)

@app.route('/')
def home():
  note1 = note.Note(1, 'user1', 'note1')
  return json.dumps(note1.__dict__)

@app.route('/register')
def register():
  return "in register"
  
@app.route('/login')
def login():
  return "in login"
  
@app.route('/add_note')
def add_note():
  return "in add_note"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)