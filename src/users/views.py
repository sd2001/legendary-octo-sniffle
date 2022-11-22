from django.shortcuts import render
from rest_framework.decorators import api_view

from backend.settings import SECRET_KEY # should be imported from .env, I have done here for better convinien
import bcrypt, jwt, datetime
from rest_framework.response import Response
from rest_framework import status
import json
from functools import wraps
import http

from .models import User
from .serializers import UserCreationSerializer, UserProfileSerializer

def token_required(f):
    @wraps(f)
    def decorated(request, *args, **kwargs):
        # print(kwargs)
        response = AuthService.get_logged_in_user(request)
        print(response.data)
        print(response.status_code)
        if response.status_code != http.HTTPStatus.OK:
            return Response({"message": 'Please provide auth token'}, status=status.HTTP_401_UNAUTHORIZED)
            
        return f(request, response.data, *args, **kwargs)

    return decorated

# Create your views here.
class AuthService:
    @staticmethod
    def check_password(password, user: User):
        """Method to check if the provided password is correct"""
        return bcrypt.checkpw(
            password.encode('utf-8'), user.password.encode('utf-8')
        )
    @staticmethod
    def __encode_auth_token__(user_id):
        try:
            payload = {"now": str(datetime.datetime.now()), "user_id": user_id}
            return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        except Exception as e:
            return e
        
    @staticmethod
    def __decode_auth_token__(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."
    
    @api_view(('POST',))
    def login_user(request):
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email', None)
        password = data.get('password', None)
        if not email or not password:
            return Response({"message": 'Missing Input Parameters'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email)[0]
        
        if not user:
            return Response({"message": 'User not Found'}, status=status.HTTP_400_BAD_REQUEST)
        print(user.first_name)
        if AuthService.check_password(password, user):
            jwt_token = AuthService.__encode_auth_token__(user.id)
            if jwt_token:
                return Response({
                    "token": str(jwt_token),
                    "user_id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": 'Some error occurred'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": 'Incorrect credentials'}, status=status.HTTP_400_BAD_REQUEST)
            
    def get_logged_in_user(request):
        auth_header = request.headers.get("Authorization")

        if auth_header:
            auth_token = auth_header.split(" ")[1]
            resp = AuthService.__decode_auth_token__(auth_token)
            if not isinstance(resp, str):
                user = User.objects.filter(id=resp)[0]
                if user:
                    data = {
                        "user_id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "token": auth_token
                    }
                    return Response(data, status=status.HTTP_200_OK)

            data = {"message": resp}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {"message": "Provide a valid auth token."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        
class UserService:
    @api_view(('POST',))
    def create_user(request):
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        user = User.objects.filter(email=data['email'])[:1]
        if user:
            return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(data['password'].encode('utf-8'), salt).decode('utf8')
        user_instance = User.objects.create(first_name=data['first_name'],
                                            last_name=data['last_name'],
                                            email=data['email'],
                                            password=hashed,
                                            password_salt=salt)
        user_instance.save()
        user_details = UserCreationSerializer(user_instance)
        return Response(user_details.data, status=status.HTTP_200_OK)
    
    @api_view(('GET',))
    @staticmethod
    @token_required
    def get_user(request, user_data):
        user = User.objects.raw(f"""select id, first_name, last_name, email,
                                        (select count(*) from social_follow where user_followed={user_data['user_id']}) as followers,
                                        (select count(*) from social_follow where user_who_followed={user_data['user_id']}) as following
                                    from users_user
                                        where id={user_data['user_id']}""")[0]
        
        user = UserProfileSerializer(user)
        return Response(user.data, status=status.HTTP_200_OK)
        
        