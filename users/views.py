from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials
import os
import json

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class GoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if not firebase_admin._apps:
            cred_json = os.environ.get('FIREBASE_CREDENTIALS_JSON')
            if cred_json is None:
                return Response({'detail': 'FIREBASE_CREDENTIALS_JSON env variable not set'}, status=500)
            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        id_token = request.data.get('id_token')
        if not id_token:
            return Response({'detail': 'No ID token provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            email = decoded_token.get('email')
            uid = decoded_token.get('uid')
            name = decoded_token.get('name', '')
            first_name = name.split(' ')[0] if name else ''
            last_name = ' '.join(name.split(' ')[1:]) if name and len(
                name.split(' ')) > 1 else ''
            User = get_user_model()
            user, created = User.objects.get_or_create(email=email, defaults={
                'username': email,
                'first_name': first_name,
                'last_name': last_name,
            })
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
