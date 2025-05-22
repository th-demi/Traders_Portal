from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, CompanyMetrics
from .serializers import CompanySerializer
from drf_yasg.utils import swagger_auto_schema
from core.throttling import SearchRateThrottle, BurstRateThrottle


class CompanyViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Company.objects.all().select_related('metrics')
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['symbol']
    search_fields = ['company_name', 'symbol']
    ordering_fields = ['company_name', 'symbol']
    ordering = ['company_name']
    throttle_classes = [SearchRateThrottle, BurstRateThrottle]

    @swagger_auto_schema(
        responses={
            200: CompanySerializer(many=True),
            400: 'Bad request',
            401: 'Unauthorized',
            500: 'Internal server error',
        },
        security=[]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
