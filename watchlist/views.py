from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from .models import Watchlist
from .serializers import WatchlistSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class WatchlistViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Handle Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return Watchlist.objects.none()
        return Watchlist.objects.filter(user=self.request.user).select_related('company')

    @swagger_auto_schema(
        responses={
            200: WatchlistSerializer(many=True),
            400: 'Bad request',
            401: 'Unauthorized',
            500: 'Internal server error',
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            201: WatchlistSerializer,
            400: 'Bad request',
            401: 'Unauthorized',
            500: 'Internal server error',
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={
            204: 'No Content',
            400: 'Bad request',
            401: 'Unauthorized',
            404: 'Not Found',
            500: 'Internal server error',
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
