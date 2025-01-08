import os
import unittest
import json

from app import create_app
from app.models import db


producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNwdWdMLWc5TURYajdhem9jOXoyWCJ9.eyJpc3MiOiJodHRwczovL2Rldi1hOHlxY2NheGlnNG41M3Z0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzQzM2E4ZjY2ODhjN2VjYzhmMjQzYjkiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNzM2MzUyMTU0LCJleHAiOjE3MzYzNTkzNTQsInNjb3BlIjoiIiwiYXpwIjoidXVwT2huc0FnQk1pZWUwWjZaeWFEN2xDYXA4UHRXa00iLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.hx5mrVNiOAH_ezpw2REpuRurq81-ujiqGgwsJ6_4Dc9J5katHzcBcmTqbPMegOS3-GC8aih6YoOEO6ziDJqiejd5lz7MMvynjMva3AfJKIeOlV5Ksu9Vrck5p-9gXKAm27UKL1TDg7sPebcBvoz_crXGcrfZNDvJOkcMdgwM2uBNtHBu0fTKfiCQz_r3QUogtwIuwETvm7aTbkmhrnKYRqOwKbB5jiUi4yDwhuXdslOZAjwPcsufaiJHUiHOAVIJ7L5M5MSF2npmqG7puPLZIhq77CMtivrSmBwAN0iqG9t6raXiaHfwgaFQ-5VmBjoGrN4lSRAL_iLHDnfz6XAyfA'
director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNwdWdMLWc5TURYajdhem9jOXoyWCJ9.eyJpc3MiOiJodHRwczovL2Rldi1hOHlxY2NheGlnNG41M3Z0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzdkNjJiMDFjZWRjYzM3NWQ3NTJhZDYiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNzM2MzUyMjgxLCJleHAiOjE3MzYzNTk0ODEsInNjb3BlIjoiIiwiYXpwIjoidXVwT2huc0FnQk1pZWUwWjZaeWFEN2xDYXA4UHRXa00iLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.ZdTc_7FXpsh2a6P7QZTTdEyy0OBZpTXb45xoW6k7Dgi6pIdZ7kUvg6BQ6DhMwUfUgvGrxDsFtjqcm4SiA4j0liyW6ZnB5Lk-klpbumTYEoGc1pgnGLZ1Xkwd87yb-j0Xopp6JsqxCmN1WjJErtdSpOGFVtj4AEeZPeucEJz_utgt85MLH0lb4gEQA6AHAasIX_8KMgfBSdv_5ucwuaq6voEVpo-QiJNp4ZQQ9OguATJO_JZAIT6aoqhdM5b5dkEkuIzIMK_H66DlCpw3sx6Xm2PU1R23aGDOxXDNZmSZruVHKxtYjfL0lc-LnNWNA02_5_H2DDMXyJp48_gLP8RO8g'
assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNwdWdMLWc5TURYajdhem9jOXoyWCJ9.eyJpc3MiOiJodHRwczovL2Rldi1hOHlxY2NheGlnNG41M3Z0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzdkNjI4ZTJlOGZmNTU3NDQ3Mzk2YmMiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNzM2MzUyMjI1LCJleHAiOjE3MzYzNTk0MjUsInNjb3BlIjoiIiwiYXpwIjoidXVwT2huc0FnQk1pZWUwWjZaeWFEN2xDYXA4UHRXa00iLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.GPqcSdugXJITGquIw6uvco9J7PTJk6Xtm0DMxiuw-7ouzkElNj54sHXixnJQ0Nwc8EXXzmxc1EfXmpYR77Jdw_zQ3QYHC2VPg5bKndKhUgW04zFfeqoMhSetME1dlIs5DjERIHUkt0AfzGvtkQvHumkqxOfy5RdFUvxRGZ2yjPBm7f1Q2CfaE2i4-bxYpR05EOlIIUiRQeq-F_OaYAti_4WsqtDVrL1tlNbSi8xEeUdiXwhZpDrhV6GtVacZfoB1EvDFwL0gLmoW6otCE0ZxcHHTBSBxS-s2DPjsnE4PyW0QEhN4SJbXRfrUIckr5XgdA6z91KEiO-8JT4x2Lr7zzw'
unverified_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNwdWdMLWc5TURYajdhem9jOXoyWCJ9'


class CastingTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_filename = "testcast.db"
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = "sqlite:///{}".format(os.path.join(self.project_dir, self.database_filename))

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            # db.drop_all()

    # Movies tests
    def test_get_movies(self):
        # get response from endpoint
        self.client
        res = self.client.get('/movies', headers={'Authorization': f'Bearer {producer_token}'})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 2)

    def test_get_movies_wrong_route_404(self):
        # get response from endpoint
        res = self.client.get('/movis', headers={'Authorization': f'Bearer {producer_token}'})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_create_movie(self):
        # get response from endpoint
        res = self.client.post('/movie', 
                               json={'title': 'Jaws', 'release_date': '1993-03-24'}, 
                               headers={'Authorization': f'Bearer {producer_token}'}
                               )

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie_no_data_422(self):
        # get response from endpoint
        res = self.client.post('/movie', 
                               headers={'Authorization': f'Bearer {producer_token}'}
                               )

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_update_movie(self):
        # get response from endpoint
        res = self.client.patch('/movie/2', 
                               json={'release_date': '1975-12-26'}, 
                               headers={'Authorization': f'Bearer {producer_token}'}
                               )

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['release_date'], '1975-12-26')

    def test_update_movie_id_not_available_404(self):
        # get response from endpoint
        res = self.client.patch('/movie/7', 
                                json={'name':'Movie'},
                               headers={'Authorization': f'Bearer {producer_token}'}
                               )

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        # get response from endpoint
        self.client
        res = self.client.delete('/movie/1', headers={'Authorization': f'Bearer {producer_token}'})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_not_available_404(self):
        # get response from endpoint
        self.client
        res = self.client.delete('/movie/10', headers={'Authorization': f'Bearer {producer_token}'})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    # Actors tests
    def test_get_actors(self):
        # get response from endpoint
        self.client
        res = self.client.get('/actors', headers={'Authorization': f'Bearer {producer_token}'})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 2)

    def test_get_actors_no_auth_401(self):
        # get response from endpoint
        self.client
        res = self.client.get('/actors')

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_actor(self):
        # get response from endpoint
        res = self.client.post('/actor', 
                               json={'name': 'Timothy Chalamet', 'age': 23, 'gender': 'M'}, 
                               headers={'Authorization': f'Bearer {producer_token}'}
                               )

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_no_age_422(self):
        # get response from endpoint
        res = self.client.post('/actor', 
                               json={'name': 'Will Smith', 'gender': 'M'}, 
                               headers={'Authorization': f'Bearer {producer_token}'}
                               )

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_update_actor(self):
        # get response from endpoint
        res = self.client.patch('/actor/2', 
                               json={'name': 'Bruce Willis', 'age': 65}, 
                               headers={'Authorization': f'Bearer {producer_token}'}
                               )

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Bruce Willis')
        self.assertEqual(data['actor']['age'], 65)

    def test_update_actor_null_data_type_422(self):
        # get response from endpoint
        res = self.client.patch('/actor/2', 
                               json={'age': None}, 
                               headers={'Authorization': f'Bearer {producer_token}'}
                               )

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


    def test_delete_actor(self):
        # get response from endpoint
        self.client
        res = self.client.delete('/actor/1', headers={'Authorization': f'Bearer {producer_token}'})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor_not_available_404(self):
        # get response from endpoint
        self.client
        res = self.client.delete('/actor/4', headers={'Authorization': f'Bearer {producer_token}'})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Authorisation Tests
    def test_create_actor_no_permission_assistant_403(self):
        # get response from endpoint
        res = self.client.post('/actor', 
                               json={'name': 'Sandra Bullock', 'age': 48, 'gender': 'F'}, 
                               headers={'Authorization': f'Bearer {assistant_token}'}
                               )

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'User does not have permission')

    def test_get_movies_assistant(self):
        # get response from endpoint
        self.client
        res = self.client.get('/movies', headers={'Authorization': f'Bearer {assistant_token}'})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 2)


    def test_create_actor_director(self):
        # get response from endpoint
        res = self.client.post('/actor', 
                               json={'name': 'Sandra Bullock', 'age': 48, 'gender': 'F'}, 
                               headers={'Authorization': f'Bearer {director_token}'}
                               )

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_no_permission_director_403(self):
        # get response from endpoint
        self.client
        res = self.client.delete('/movie/2', headers={'Authorization': f'Bearer {director_token}'})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'User does not have permission')

    def test_get_actors_unverified_token_401(self):
        # get response from endpoint
        self.client
        res = self.client.get('/actors', headers={'Authorization': f'Bearer {unverified_producer_token}'})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'User is not authenticated')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
