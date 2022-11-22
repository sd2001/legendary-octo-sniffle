from functools import wraps
from users.views import AuthService

from rest_framework.response import Response
from rest_framework import status

import http

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