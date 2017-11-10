from flask_restful import Resource, reqparse
from models.category import CategoryModel
from flask_jwt import jwt_required

class Category(Resource):
     
    @jwt_required()
    def get(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            return category.json()
        return {'message': 'Category not found'}, 404
    @jwt_required()
    def post(self, name):
        if CategoryModel.find_by_name(name):
            return {'message': "A category with name '{}' already exists.".format(name)}, 400

        category = CategoryModel(name)
        try:
            category.save_to_db()
        except:
            return {"message": "An error occurred creating the category."}, 500

        return category.json(), 201
    
    @jwt_required()
    def delete(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            category.delete_from_db()

        return {'message': 'Category deleted'}

class CategoryList(Resource):
    @jwt_required()
    def get(self):
        return {'categories': list(map(lambda x: x.json(), CategoryModel.query.all()))}
