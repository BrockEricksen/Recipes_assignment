from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/main')
def recipe_main():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/')
    current_user = User.get_current_user(session['user_id'])
    recipes = Recipe.get_all_recipes_with_owner()
    return render_template('user_main.html', user=current_user, recipes=recipes)

@app.route('/new_recipe')
def new_recipe():
    return render_template('new_recipe.html')

@app.route('/recipe/create', methods=['POST'])
def create_recipe():
    if Recipe.validator(request.form):
        Recipe.save(request.form)
        return redirect ('/main')
    return redirect('/new_recipe')

@app.route('/view_recipe/<int:id>')
def show_recipe(id):
    current_user = User.get_current_user(session['user_id'])
    recipe = Recipe.get_by_id(id)
    return render_template('view_recipe.html', recipe = recipe, user=current_user)

@app.route('/edit_recipe/<int:id>')
def edit_recipe(id):
    recipe = Recipe.get_by_id(id)
    return render_template('edit.html', recipe=recipe)

@app.route('/recipe/update/<int:id>', methods=['POST'])
def update(id):
    is_valid = Recipe.update_recipe(request.form, session['user_id'])
    if not is_valid:
        return redirect (f'/edit_recipe/{id}')
    return redirect('/main')

@app.route('/recipe/destroy/<int:id>')
def destroy(id):
    data = {
        'id': id
    }
    Recipe.destroy(data)
    return redirect('/main')