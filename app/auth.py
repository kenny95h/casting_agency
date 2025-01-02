import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-a8yqccaxig4n53vt.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
   # raise error if no authorization
    if 'Authorization' not in request.headers:
        abort(401)

    # get the authorization string
    auth_header = request.headers['Authorization']

    # split at space and take the second index to remove 'Bearer'
    auth= auth_header.split(' ')

    # validate the authorization string as a bearer with token
    if len(auth) != 2 or auth[0].lower() != 'bearer':
        abort(401)

    # return JWT
    return auth[1]

def check_permissions(permission, payload):
    # confirm payload contains the permissions key
    if 'permissions' not in payload:
        abort(400)
    
    # confirm permission we are requesting exists in user payload
    if permission not in payload['permissions']:
        abort(403)
    
    # return True if user has the required permission
    return True

def verify_decode_jwt(token):
    # load data from Auth0 url
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # get the header data from token
    unverified_header = jwt.get_unverified_header(token)
    
    # check data is in header
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    # check key ids match in token and auth0 account
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # decode and validate the JWT using the users token and key from Auth0
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            # return payload if response is valid
            return payload
        
        # raise errors based on payload response if payload is not valid
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # check JWT is valid
            jwt = get_token_auth_header()
            try:
                # verify JWT with Auth0
                payload = verify_decode_jwt(jwt)
            except:
                abort(401)
            # check JWT includes required permission
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator