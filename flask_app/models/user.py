from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'recipes' # make a variable to use in the result variable that uses the database's name instead of typing out each instance

    def __init__(self, data): # constructor method to make the database key info to be accessable by the templates
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes_created = []

    @classmethod
    def create_user(cls, data): #this is a method to save a new users information into our database
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        if result == ():
            return False
        return cls(result[0])
    
    @classmethod
    def get_current_user(cls, user_id):
        data = {
            'id': user_id
        }
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_create(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters long.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters long.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invald email address.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long.")
            is_valid = False
        if user['password'] != user['conf_password']:
            flash("Passwords do not match.")
            is_valid = False
        data = {
            'email': user['email']
        }
        user_in_db = User.get_by_email(data)
        if user_in_db:
            flash("Email already taken.")
            is_valid = False
        return is_valid