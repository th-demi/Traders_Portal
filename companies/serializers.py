from rest_framework import serializers
from .models import Company, CompanyMetrics


class CompanySerializer(serializers.ModelSerializer):
    pe = serializers.FloatField(source='metrics.pe', read_only=True)
    roe_ttm = serializers.FloatField(source='metrics.roe_ttm', read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'company_name', 'symbol',
                  'scripcode', 'pe', 'roe_ttm']
