from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import matches
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = "solo_project"


    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.age = data['age']
        self.city = data['city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# Save
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( first_name , last_name , email ,password,age ) VALUES ( %(first_name)s , %(last_name)s , %(email)s ,%(password)s,%(age)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db(query, data)





#Validate
    @staticmethod
    def validate_user(user_data):
        required_keys = ['first_name', 'last_name', 'email', 'password']

    # Check that all required keys are present in the form data
        if not all(key in user_data for key in required_keys):
            return False

    # Validate each field according to your requirements
        if len(user_data['first_name']) < 2:
            return False

        if len(user_data['last_name']) < 2:
            return False

    # Validate the email using a regular expression
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, user_data['email']):
            return False

        if len(user_data['password']) < 6:
            return False

        return True

    @classmethod
    def get_user_by_id(cls, users_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {
            "id": users_id
        }
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return None
        return cls(result[0])

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for u in results:
            users.append(cls(u))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)

    
    # @staticmethod
    # def validate_user(user):
    #     query = "SELECT * FROM users WHERE email = %(email)s;"
    #     result = connectToMySQL(User.DB).query_db(query, user)
    #     is_valid = True  
    #     if len(user['first_name']) < 2:
    #         flash("First name should be at least 2 characters.")
    #         is_valid = False
        

    #     if len(user['last_name']) < 2:
    #         flash("Last name should be at least 3 characters.")
    #         is_valid = False
        

    #     if len(user['email']) == 0:
    #         flash("Email is required.")
    #         is_valid = False
    #     if not EMAIL_REGEX.match(user['email']): 
    #         flash("Invalid email format.")
    #         is_valid = False
    #     if len(result) >=1:
    #         flash("Email already in use.")
    #         is_valid = False

    #     if len(user['password']) < 8:
    #         flash("Password should be at least 8 characters.")
    #         is_valid = False

    #     if user['password'] != user['confirm_password']:
    #         flash("Passwords do not match.")
    #         is_valid = False
    #     if len(user['age']) < 18:
    #         flash("too young.")
    #         is_valid = False
    #     return is_valid



    @staticmethod
    def validate_user(user):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(User.DB).query_db(query, user)
        is_valid = True

        if len(user['first_name']) < 2:
            flash("First name should be at least 2 characters.")
            is_valid = False

        if len(user['last_name']) < 2:
            flash("Last name should be at least 2 characters.")
            is_valid = False

        if len(user['email']) == 0:
            flash("Email is required.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email format.")
            is_valid = False
        if len(result) >= 1:
            flash("Email already in use.")
            is_valid = False

        if len(user['password']) < 8:
            flash("Password should be at least 8 characters.")
            is_valid = False

        if user['password'] != user['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False

        age = user['age']
        if not age.isdigit() or int(age) < 18:
            flash("You must be 18 years or older to join.")
            is_valid = False

        return is_valid

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])