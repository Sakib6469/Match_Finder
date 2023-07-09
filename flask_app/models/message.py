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
        self.user_id_sender = data['user_id_sender']
        self.user_id_recipient = data['user_id_recipient']
        self.created_at = data['created_at']


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM message WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return False
        return cls(result[0])