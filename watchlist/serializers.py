from rest_framework import serializers
from .models import Watchlist
from companies.serializers import CompanySerializer


class WatchlistSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(queryset=Watchlist._meta.get_field(
        'company').related_model.objects.all(), write_only=True, source='company')

    class Meta:
        model = Watchlist
        fields = ['id', 'company', 'company_id', 'added_at']
