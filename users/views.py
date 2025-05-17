from django.shortcuts import render
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    LoginSerializer,
    UserSerializer,
    UserCreateSerializer
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from core.throttling import AuthRateThrottle, BurstRateThrottle

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer
    throttle_classes = [AuthRateThrottle]

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
        return Response({
            'user': UserProfileSerializer(user).data,
            'message': 'Registration successful. Please log in.'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = [AuthRateThrottle]

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
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if not user:
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [BurstRateThrottle]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        throttle_classes = [AuthRateThrottle]
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
