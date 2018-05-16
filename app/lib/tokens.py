import jwt 
import datetime
from config import PRIVATE_KEY

def encode_jwt_token(profile_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': profile_id
        }
        return jwt.encode(
            payload,
            PRIVATE_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_jwt_token(auth_token):
    try:
        payload = jwt.decode(auth_token, PRIVATE_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'