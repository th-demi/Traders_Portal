from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserRegistrationSerializer, UserProfileSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={
            201: 'Registration successful',
            400: 'Bad request (validation error)',
            500: 'Internal server error',
        },
        security=[]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Do NOT issue JWT tokens here. Only return user info.
        return Response({
            'user': UserProfileSerializer(user).data,
            'message': 'Registration successful. Please log in.'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: 'Login successful',
            400: 'Bad request (missing fields)',
            401: 'Unauthorized (invalid credentials)',
            500: 'Internal server error',
        },
        security=[]
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            # Do not log sensitive info
            return Response({
                'error': 'Please provide both username and password.'
            }, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            # Do not reveal if username or password is wrong
            return Response({
                'error': 'Invalid credentials.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

# Note: The token refresh endpoint is handled by rest_framework_simplejwt.views.TokenRefreshView, not by any custom logic in this file.
