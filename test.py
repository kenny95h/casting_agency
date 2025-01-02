import os
import unittest
import json

from app import create_app
from app.models import db


producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNwdWdMLWc5TURYajdhem9jOXoyWCJ9.eyJpc3MiOiJodHRwczovL2Rldi1hOHlxY2NheGlnNG41M3Z0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzQzM2E4ZjY2ODhjN2VjYzhmMjQzYjkiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNzM1ODQwMDQ1LCJleHAiOjE3MzU4NDcyNDUsInNjb3BlIjoiIiwiYXpwIjoidXVwT2huc0FnQk1pZWUwWjZaeWFEN2xDYXA4UHRXa00iLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.ha5ZBG2_6JpYwYLmOgfG2G_LXDwNE4I5U8-KVIgQ8R39cqOBhSDZK3TU8vLC08s5jhqHX0pyDO75YVyTEXuUuFvNlCPsjatYIwFnq3pfHa4pCrH8VPMiCBXdJB-cuFk0neiZu6KGKwwRGcqr0111nnDchAq7mxAPXBYDiIZ0mYCr4tbHCqlcYtuKTHe6-NXLCqfkyNu6NIiPTVUKlrRRKNmU0w8a4pIqOkytmVEtJe_AAF3OfJiHJJKpGmMdyRpEFlFh2iXSeCF7P802hce8r0KX7faFduK-Vi1XwImdyP-F7PfBr83r6qFYBem3aZqofmRcn7dhy2OmNx4cN-uBRw'
director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNwdWdMLWc5TURYajdhem9jOXoyWCJ9.eyJpc3MiOiJodHRwczovL2Rldi1hOHlxY2NheGlnNG41M3Z0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzY1NWVjNmMyNGE0MDQ5MTRkNGI3MTciLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNzM1ODQyMjQ2LCJleHAiOjE3MzU4NDk0NDYsInNjb3BlIjoiIiwiYXpwIjoidXVwT2huc0FnQk1pZWUwWjZaeWFEN2xDYXA4UHRXa00iLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.n60e6obOeQjj68f4wYqf_E-igqNiTeHfv0bNGsuc_zbxbgtyQuI4NhoM9emSHRnGX-7pWW1Zgv5f1j7ANnaDOWE1eBfNKqJZFGfZhu9474zkZ6G7rwuH_lJ0a3C4E5wpWuVsB2y03G3x3sqmLY3yuk6CIOSuVDaypL9KlcaUxowpXDDUSUfcBPpHyZtkF-x3NDYqrbcc-OWtN8LKl0Db3-LANrZrywmmTZEiEou0QsC_MlcAyTUdlg62tbEwNxgIo0vQIQavCPHpl_rUg4Ll1vgLb9xK2OSVwQ9q1ikRmQX_POLbe3H2IRHn9NXp-hVy9xlgAU0hpRO-_Uaz7qV7UQ'
assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNwdWdMLWc5TURYajdhem9jOXoyWCJ9.eyJpc3MiOiJodHRwczovL2Rldi1hOHlxY2NheGlnNG41M3Z0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzQzM2FiYWIzYWM3YmI4NmMzMWE3ZDAiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNzM1ODQyMzAxLCJleHAiOjE3MzU4NDk1MDEsInNjb3BlIjoiIiwiYXpwIjoidXVwT2huc0FnQk1pZWUwWjZaeWFEN2xDYXA4UHRXa00iLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.j6AUIxFdOcvdRIpZ5j6usGV5y_AQ30WUAs4J7VXuanXn1cYytB2oQwlKuFNTtQE3WWIb_cAIny_ZetaAOkp_QbM8oK6sIMb5es4uMIwF3kBWBD_cnzmIRwB3rF8kbsFB-3pwkweu2q_fjYDaU_HJVUYhxdsjJCi2BrkXL2vCLNAAN8B9MaQlvuF0vFUdCwZz054_oAWfsbOePGBbm3-vrwmPYvKEixkQjez_Kg1fpERbrpS59hYQZtTnry00IEd1N4BDL4aJLN74PlFvvj9m94wlm-E0aDlLJunfTGpLapT53G0MmrF8kV_u7xJd-V6fVJXgfVuXHFFnKEgffhBxnA'
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
