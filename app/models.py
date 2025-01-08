import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
import app.config as config

database_path = config.database_path

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    movie = Movie(
        title='Avatar',
        release_date='2024-12-11'
    )

    movie.insert()

    movie = Movie(
        title='Elf',
        release_date='2009-08-21'
    )

    movie.insert()
    
    actor = Actor(
        name='Kirsten Bell',
        age=32,
        gender='F'
    )
    
    actor.insert()

    actor = Actor(
        name='Bruce Wills',
        age=63,
        gender='M'
    )
    
    actor.insert()

class Movie(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(120), nullable=False)
    release_date = Column(String(60), nullable=False)

    def desc(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.desc)

class Actor(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(60), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(1), nullable=False)

    def desc(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.desc)