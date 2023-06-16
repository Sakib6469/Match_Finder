from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Match:
    DB = "solo_project"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.city = data['city']
        self.description = data['description']
        self.picture = data['picture']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users = []

    
    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO matches (first_name,last_name,age,city,description,picture,user_id)
                VALUES (%(first_name)s,%(last_name)s,%(age)s,%(city)s,%(description)s,%(picture)s,%(user_id)s);
                """
        return connectToMySQL(cls.DB).query_db(query, form_data)


    @staticmethod
    def validate(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash('First name must be at least 2 characters.')
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash('Last name must be at least 2 characters.')
            is_valid = False
        if not form_data['age'].isdigit() or int(form_data['age']) < 18:
            flash('Age must be a number greater than or equal to 18.')
            is_valid = False
        if len(form_data['city']) < 2:
            flash('City name must be at least 2 characters.')
            is_valid = False
        if len(form_data['description']) < 10:
            flash('Description must be at least 10 characters.')
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM matches LEFT JOIN users ON matches.user_id = users.id;
    """
        result = connectToMySQL(cls.DB).query_db(query)
        if not result:
            return None
        matches_list = []
        for row in result:
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": "",
                "age": row["age"],
                "city": row["city"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
            }
            matches_data = {
                "id": row["id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "age": row["age"],
                "city": row["city"],
                "description": row["description"],
                "picture": row["picture"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "user": user_data,
            }
            matches = cls(matches_data)
            matches_list.append(matches)
        return matches_list

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM matches WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM matches
                JOIN users on matches.user_id = users.id
                WHERE matches.id = %(id)s;
                """
        result = connectToMySQL(cls.DB).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_matches = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "age": result['age'],
                "city": result['city'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_matches.creator = users.User(user_data)
        return this_matches

    @classmethod
    def get_one(cls, data):
        query = """
    SELECT * FROM matches
    LEFT JOIN users ON matches.user_id = users.id
    WHERE matches.id = %(id)s;
    """
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return None
        matches_data = result[0]
        matches = cls(matches_data)
        for row in result:
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "age": row["age"],
                "city": row["city"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
            }
            user = next((u for u in matches.users if u.id == user_data['id']), None)
            if user is None:
                user = users.User(user_data)
                matches.users.append(user)
        return matches




    @classmethod
    def update(cls, form_data):
        query = """
                UPDATE matches
                SET first_name = %(first_name)s,
                last_name = %(last_name)s,
                city = %(city)s,
                age = %(age)s,
                description = %(description)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.DB).query_db(query, form_data)