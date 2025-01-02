import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from app.auth import requires_auth
from app.models import Actor, Movie, db_drop_and_create_all, setup_db


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)
        with app.app_context():
            db_drop_and_create_all()

    CORS(app)

    with app.app_context():
        db_drop_and_create_all()

    # ROUTES

    '''
        GET: Movies
    '''
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        # get all movies
        movies = Movie.query.all()

        # create list of movies
        movie_list = []
        for movie in movies:
            movie_list.append(movie.desc())

        return jsonify({
            'success': True,
            'movies': movie_list
        }), 200

    '''
        DELETE: Movie
    '''
    @app.route('/movie/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(jwt, id):
        # get movie with given ID
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        # raise error if no movie with given ID
        if movie is None:
            abort(404)
        try:
            # delete the movie
            movie.delete()

            return jsonify({
                "success": True
            }),200
        except:
            abort(422)

    '''
        POST: Movie
    '''
    @app.route('/movie', methods=['POST'])
    @requires_auth('post:movie')
    def create_movie(jwt):
        try:
            # get request JSON data
            body = request.get_json()
            title = body.get("title")
            release = body.get("release_date")

            # create new movie
            movie = Movie(title=title, release_date=release)
            movie.insert()

            return jsonify({
                "success": True,
                'movie': movie.desc()
            }),200
        except:
            abort(422)

    '''
        PATCH: Movie
    '''
    @app.route('/movie/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(jwt, id):
        # get movie with given ID
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        # get passed in JSON data
        body = request.get_json()

        # raise error if no movie with given ID
        if movie is None:
            abort(404)
        try:
            # check if title or release date has been passed and update
            if 'title' in body:
                title = body.get("title")
                movie.title = title
            if 'release_date' in body:
                release = body.get("release_date")
                movie.release_date = release

            # overwrite existing actor details with new data  
            movie.update()

            return jsonify({
                "success": True,
                'movie': movie.desc()
            }),200
        except:
            abort(422)

    '''
        GET: Actors
    '''
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        # get all actors
        actors = Actor.query.all()

        # create list of actors
        actor_list = []
        for actor in actors:
            actor_list.append(actor.desc())

        return jsonify({
            'success': True,
            'actors': actor_list
        }), 200

    '''
        DELETE: Actor
    '''
    @app.route('/actor/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(jwt, id):
        # get actor with given ID
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        # raise error if no actor with given ID
        if actor is None:
            abort(404)
        try:
            # delete the actor
            actor.delete()

            return jsonify({
                "success": True
            }),200
        except:
            abort(422)

    '''
        POST: Actor
    '''
    @app.route('/actor', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor(jwt):
        try:
            # get request JSON data
            body = request.get_json()
            name = body.get("name")
            age = body.get("age")
            gender = body.get("gender")


            # create new actor
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            return jsonify({
                "success": True,
                'actor': actor.desc()
            }),200
        except:
            abort(422)

    '''
        PATCH: Actor
    '''
    @app.route('/actor/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(jwt, id):
        # get actor with given ID
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        # get passed in JSON data
        body = request.get_json()

        # raise error if no actor with given ID
        if actor is None:
            abort(404)
        try:
            # check if name, age or gender has been passed and update
            if 'name' in body:
                name = body.get("name")
                actor.name = name
            if 'age' in body:
                age = body.get("age")
                actor.age = age
            if 'gender' in body:
                gender = body.get("gender")
                actor.gender = gender

            # overwrite existing actor details with new data  
            actor.update()

            return jsonify({
                "success": True,
                'actor': actor.desc()
            }),200
        except:
            abort(422)

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(403)
    def nopermission(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "User does not have permission"
        }), 403

    @app.errorhandler(401)
    def notauthenticated(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "User is not authenticated"
        }), 401

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False, 
                "error": 400, 
                "message": "Bad request"
            }),
        400)
    
    return app
    
app = create_app()

if __name__ == '__main__':
    app.run()