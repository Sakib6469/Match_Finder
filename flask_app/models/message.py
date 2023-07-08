from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users
from flask_app.models import matches
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Message:
    DB = "solo_project"
    def __init__(self,data):
        self.id = data['id']
        self.text = data['text']
        self.created_at = data['created_at']
        