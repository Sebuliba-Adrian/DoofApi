from db import db

class RecipeModel(db.Model):
    __tablename__ = 'recipies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    instructions= db.Column(db.String(1000))

    recipe_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    recipe = db.relationship('CategoryModel')

    def __init__(self, name, instructions, recipe_id):
        self.name = name
        self.instructions= instructions
        self.recipe_id = recipe_id

    def json(self):
        return {'name': self.name, 'instructions': self.instructions}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
