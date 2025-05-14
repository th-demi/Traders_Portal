from rest_framework.routers import DefaultRouter
from companies.views import CompanyViewSet
from watchlist.views import WatchlistViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')

urlpatterns = [
    path('', include(router.urls)),
] 