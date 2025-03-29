from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.shortcuts import redirect
from .serializers import *

from rest_framework.permissions import IsAuthenticated
# from authorsHaven.utils import custom_success_response
from django.conf import settings
from rest_framework.response import Response


EMAIL_HOST_USER = settings.EMAIL_HOST_USER

def pageLogout(request):
    if request.method == "POST":
        
        logout(request)
        response=redirect('home')
        response.delete_cookie('login_token')
        return response


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """
    Create a new user account.
    """
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_account(request):
    """
    Retrieve the currently authenticated user's account details.
    """
    serializer = CreateUserSerializer(request.user)
    return Response(serializer.data)


"""User Sing-in process
required field: username['email'], password
"""
class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    

@api_view(['POST'])
def debug_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Direct database check
    from users.models import User
    try:
        user_db = User.objects.get(username=username)
        print(f"Found user in DB: {user_db.username}")
        
        # Check password directly
        from django.contrib.auth.hashers import check_password
        pwd_valid = check_password(password, user_db.password)
        print(f"Password valid: {pwd_valid}")
        
        # Try standard authentication
        from django.contrib.auth import authenticate
        auth_user = authenticate(username=username, password=password)
        print(f"Auth result: {auth_user}")
        
        if auth_user:
            # Success!
            from rest_framework.authtoken.models import Token
            token, _ = Token.objects.get_or_create(user=auth_user)
            return Response({
                'success': True,
                'token': token.key
            })
        else:
            return Response({
                'success': False,
                'error': 'Authentication failed',
                'user_exists': True,
                'password_valid': pwd_valid
            }, status=400)
            
    except User.DoesNotExist:
        return Response({
            'success': False,
            'error': 'User not found',
            'tried_username': username
        }, status=400)

