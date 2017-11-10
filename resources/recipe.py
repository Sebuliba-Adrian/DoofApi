from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.recipe import RecipeModel

class Recipe(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('instructions',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('category_id',
        type=int,
        required=True,
        help="Every recipe needs a category_id."
    )

    @jwt_required()
    def get(self, name):
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            return recipe.json()
        return {'message': 'Recipe not found'}, 404

    @jwt_required()
    def post(self, name):
        if RecipeModel.find_by_name(name):
            return {'message': "A recipe with name '{}' already exists.".format(name)}, 400

        data = Recipe.parser.parse_args()

        recipe = RecipeModel(name, data['instructions'], data['category_id'])

        try:
            recipe.save_to_db()
        except:
            return {"message": "An error occurred inserting the recipe."}, 500

        return recipe.json(), 201
    
    @jwt_required()
    def delete(self, name):
        recipe = RecipeModel.find_by_name(name)
        if recipe:
            recipe.delete_from_db()

        return {'message': 'Recipe deleted'}

    def put(self, name):
        data = Recipe.parser.parse_args()

        recipe = RecipeModel.find_by_name(name)

        if recipe:
            recipe.instructions = data['instructions']
        else:
            recipe = RecipeModel(name, data['instructions'])

        recipe.save_to_db()

        return recipe.json()

class RecipeList(Resource):
    def get(self):
        return {'recipes': list(map(lambda x: x.json(), RecipeModel.query.all()))}
