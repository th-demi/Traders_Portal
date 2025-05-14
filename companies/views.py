from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Company
from .serializers import CompanySerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['symbol']
    search_fields = ['company_name', 'symbol']
    ordering_fields = ['company_name', 'symbol']
    ordering = ['company_name']
