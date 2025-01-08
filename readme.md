# Capstone Project

## Casting Agency API

### Getting Started

* Base URL:
  * The app is hosted through the Render cloud platform at `https://casting-agency-0o8z.onrender.com/`
  * If running locally, the app is hosted at the default, `http://127.0.0.1:5000/`, and is a Flask-based app. The database is hosted on as a local postgres db, therefore the `config.py` file must be updated with your local postgres database name and password to allow the database to be setup with required tables. To install the dependencies `cd` to the casting_agency folder, then `pip install -r requirements.txt`, and then start the Flask app by setting the env `export FLASK_APP=app`, then `export FLASK_ENV=development`, and run the app with `flask run`
  * To test the application the unit tests script can be ran with `python3 test.py`, this will run all unit tests displaying the number of successful test runs. As the endpoints require permissions to access, the variables within the test script that hold the bearer tokens for each of the three roles will need to be updated with a valid bearer token.
* Authentication: This version of the application requires authentication to successfully use the API, without providing a bearer token with the required permissions connecting to the API endpoints will give a `401 Auth Error`. The app uses Auth0 to register users and attach specified roles for accessing the API. The three roles provide permissions to access different endpoints, as such:
  * Assistant:
    * GET '/movies'
    * GET '/actors'
  * Director:
    * All permissions assistants have
    * POST '/actor/<id>'
    * PATCH '/actor/<id>'
    * DELETE '/actor/<id>'
    * PATCH '/movie/<id>'
  * Producer:
    * All permissions directors have
    * POST '/movie/<id>'
    * DELETE '/movie/<id>'
* By going to the following address for the casting service Auth0 application and logging in with a registered user, this will then return a new bearer token in the URI for this user which can be used to authenticate the API.
  * [Log in | CastingService](https://dev-a8yqccaxig4n53vt.us.auth0.com/authorize?audience=casting&response_type=token&client_id=uupOhnsAgBMiee0Z6ZyaD7lCap8PtWkM&redirect_uri=https://127.0.0.1:5000/)
  * Assistant test login: assistanttestlogin@castingapp.com AssistantPassword!
  * Producer test login: producertestlogin@castingapp.com ProducerPassword!
  * Director test login: directortestlogin@castingapp.com DirectorPassword!

### Error Handling

Errors are returned as JSON objects in the following format: { "success": False, "error": 404, "message": "Resource not found" }

The API will return four error types when requests fail:

* 400: Bad Request
* 401: User is not authenticated
* 403: User does not have permission
* 404: Resource Not Found
* 422: Request contains invalid data
* 500: Server error

### Endpoints

`GET '/movies'`

* Fetches a list of movies including the unique id, release date and title of each movie

* Returns: An object with a key, `movies`, that contains a list of all movies, and a key, `success`, with value `true`

Sample: `curl https://casting-agency-0o8z.onrender.com/movies -H "Authorization: Bearer {token}"`

```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "2024-12-11",
            "title": "Avatar"
        },
        {
            "id": 2,
            "release_date": "2009-08-21",
            "title": "Elf"
        }
    ],
    "success": true
}
```

`POST '/movie'`

* Creates a new movie using the submitted title and release date. Request body:

```json
{
    "title":"Castway",
    "release_date":"2001-01-10"
}
```

* Returns: An object with a key, `movie`, that contains the new movie object, and a key, `success`, with value `true`

Sample: `curl https://casting-agency-0o8z.onrender.com/movie -X POST -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"title":"Castway", "release_date":"2001-01-10"}'`

```json
{
    "movie": {
        "id": 3,
        "release_date": "2001-01-10",
        "title": "Castway"
    },
    "success": true
}
```

`PATCH '/movie/{movie_id}'`

* Updates a movie with given id, if exists, using the submitted data. This can include title and/or release date values to be updated. Request body:

```json
{
    "title":"Castaway",
    "release_date":"2001-01-12"
}
```

* Returns: An object with a key, `movie`, that contains the existing movie object with updated data, and a key, `success`, with value `true`

Sample: `curl https://casting-agency-0o8z.onrender.com/movie/3 -X PATCH -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"title":"Castaway", "release_date":"2001-01-12"}`

```json
{
    "movie": {
        "id": 3,
        "release_date": "2001-01-12",
        "title": "Castaway"
    },
    "success": true
}
```

`DELETE '/movie/{movie_id}'`

* Deletes a movie with given id, if exists

* Returns: A single key `success` with value `true`

Sample: `curl https://casting-agency-0o8z.onrender.com/movie/3 -X DELETE -H "Authorization: Bearer {token}"`

```json
{
    "success": true
}
```

`GET '/actors'`

* Fetches a list of actors including the unique id, age, gender and name of each actor

* Returns: An object with a key, `actors`, that contains a list of all actors, and a key, `success`, with value `true`

Sample: `curl https://casting-agency-0o8z.onrender.com/actors -H "Authorization: Bearer {token}"`

```json
{
    "actors": [{
        "age": 32,
        "gender": "F",
        "id": 1,
        "name": "Kirsten Bell"
    }, {
        "age": 63,
        "gender": "M",
        "id": 2,
        "name": "Bruce Wills"
    }],
    "success": true
}
```

`POST '/actor'`

* Creates a new actor using the submitted name, age and gender. Request body:

```json
{
    "age": 27,
    "gender": "F",
    "name": "Tom Hooland"
}
```

* Returns: An object with a key, `actor`, that contains the new actor object, and a key, `success`, with value `true`

Sample: `curl https://casting-agency-0o8z.onrender.com/actor -X POST -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"age": 27, "gender": "F", "name": "Tom Hooland"}'`

```json
{
    "actor": {
        "age": 27,
        "gender": "F",
        "id": 3,
        "name": "Tom Hooland"
    },
    "success": true
}
```

`PATCH '/actor/{actor_id}'`

* Updates an actor with given id, if exists, using the submitted data. This can include age, gender and/or name values to be updated. Request body:

```json
{
    "age": 28,
    "gender": "M",
    "name": "Tom Holland"
}
```

* Returns: An object with a key, `actor`, that contains the existing actor object with updated data, and a key, `success`, with value `true`

Sample: `curl https://casting-agency-0o8z.onrender.com/actor/3 -X PATCH -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d '{"age": 28, "gender": "M", "name": "Tom Holland"}'`

```json
{
    "actor": {
        "age": 28,
        "gender": "M",
        "id": 3,
        "name": "Tom Holland"
    },
    "success": true
}
```

`DELETE '/actor/{actor_id}'`

* Deletes an actor with given id, if exists

* Returns: A single key `success` with value `true`

Sample: `curl https://casting-agency-0o8z.onrender.com/actor/3 -X DELETE -H "Authorization: Bearer {token}"`

```json
{
    "success": true
}
```





