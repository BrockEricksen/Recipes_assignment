from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Recipe:
    db = 'recipes' # make a variable to use in the result variable that uses the database's name instead of typing out each time

    def __init__(self, data): # constructor method to make the database key info to be accessable by the templates
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None

    @classmethod
    def save(cls, data):
        if not cls.validator(data):
            return False
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s);"
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        return result
    
    @classmethod
    def get_all_recipes_with_owner(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)
            one_recipe_owner_info = {
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            owner = user.User(one_recipe_owner_info)
            one_recipe.owner = owner
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def update_recipe(cls, recipe_dict, session_id):
        recipe = cls.get_by_id(recipe_dict['id'])
        if recipe.user.id != session_id:
            flash("You do not own this recipe.")
            return False
        if not cls.validator(recipe_dict):
            return False
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under_30=%(under_30)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, recipe_dict)
        recipe = cls.get_by_id(recipe_dict['id'])
        return recipe

    @classmethod
    def get_by_id(cls, recipe_id):
        data = {
            'id': recipe_id
            }
        query = "SELECT * FROM recipes JOIN users on users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        result = result[0]
        recipe = cls(result)
        recipe.user = user.User({
                    "id": result["user_id"],
                    "first_name": result["first_name"],
                    "last_name": result["last_name"],
                    "email": result["email"],
                    "password": result["password"],
                    "created_at": result["created_at"],
                    "updated_at": result["updated_at"]
                })
        return recipe

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validator(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters long.")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters long.")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions must be at least 3 characters long.")
            is_valid = False
        if len(data['date_made']) <= 0:
            flash("Please select a date for when this was made/created.")
            is_valid = False
        if 'under_30' not in data:
            flash("Please select 'Yes' or 'No' for if this recipe takes less than 30 minutes.")
            is_valid = False
        return is_valid