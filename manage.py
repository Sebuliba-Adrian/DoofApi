from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.recipe import Recipe, RecipeList
from resources.category import Category, CategoryList
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__,instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Now you cant see me'
api = Api(app)

@app.before_first_request

def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Category, '/category/<string:name>')
api.add_resource(CategoryList, '/categories')
api.add_resource(Recipe, '/recipe/<string:name>')
api.add_resource(RecipeList, '/recipes')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    manager.run()
