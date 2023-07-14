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
        self.user_id_recipient = data['user_id_sender']
        self.created_at = data['created_at']


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM message WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def get_users_messages(cls, user_id):
        data = { 'id' : user_id}
        query = """
        SELECT * FROM messages WHERE id = %(user_id_sender)s,%(user_id_sender)s
        ;"""

#write query to get all messages associated with user's id as recipient and sort by create_at

        # get all messages sent to user 
        # get all messages sent to or from user 
        # get all users that user has a message history with 
        # get all messages where user_id and coorespondents id match 

    @classmethod
    def get_message_by_id(cls, message_id):
        data = { 'id' : message_id}
        query = """
          SELECT * 
        FROM message 
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    # Save
    @classmethod
    def save(cls, data):
        query = "INSERT INTO message (text,) VALUES ( %(text)s);"
        return connectToMySQL(cls.DB).query_db(query, data)
