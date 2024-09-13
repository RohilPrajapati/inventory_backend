from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from backend.settings import SIMPLE_JWT
import jwt
from random import randrange

# from user.models import ResetToken


def get_token(user):
    refresh = RefreshToken.for_user(user)
    refresh.access_token['role'] = user.role.name
    refresh['role'] = user.role.name
    return {
    'access': str(refresh.access_token),
    'refresh': str(refresh)
    }

def decode_token(request):
    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    user , token = response
    payload = jwt.decode(str(token),SIMPLE_JWT['SIGNING_KEY'],SIMPLE_JWT['ALGORITHM'])
    return payload

# def get_OTP():
#     OTP = randrange(10)
#     for i in range (0,5):
#         letter = randrange(10)
#         OTP= OTP*10
#         OTP = OTP + letter
#         # print(letter)
#     if ResetToken.objects.filter(OTP=OTP).exists():
#         get_OTP()
#     return OTP
