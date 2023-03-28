from flask import Flask, request, jsonify
import requests

base_url = 'https://api.spoonacular.com/recipes/complexSearch'
api_key = '<b48b5e60846d4b30a85b088991df1ccf>'

app = Flask(__name__)

@app.route('/recipes')
def suggest_recipe():
    ingredients = request.args.get('ingredients')
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=1&apiKey={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"status": "failure", "code": response.status_code, "message": response.text})

    recipe_id = response.json()[0]['id']
    recipe_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}"
    recipe_response = requests.get(recipe_url)

    if recipe_response.status_code != 200:
        return jsonify({"status": "failure", "code": recipe_response.status_code, "message": recipe_response.text})

    recipe_data = recipe_response.json()
    recipe_title = recipe_data['title']
    recipe_image = recipe_data['image']
    recipe_ingredients = recipe_data['extendedIngredients']
    recipe_instructions = recipe_data['analyzedInstructions'][0]['steps']

    return jsonify({"title": recipe_title, "image": recipe_image, "ingredients": recipe_ingredients, "instructions": recipe_instructions})



if __name__ == '__main__':
    app.run()
