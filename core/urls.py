from rest_framework.routers import DefaultRouter
from companies.views import CompanyViewSet
from watchlist.views import WatchlistViewSet
from django.urls import path, include
from .views import (
    home_view, company_list_view, watchlist_view,
    add_to_watchlist, remove_from_watchlist,
    login_view, register_view, logout_view,
    google_login_view, google_login_callback
)

# API routes
router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company-api')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist-api')

# URL patterns for both API and SSR views
urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),

    # SSR pages
    path('', home_view, name='home'),
    path('companies/', company_list_view, name='company_list'),
    path('watchlist/', watchlist_view, name='watchlist'),
    path('companies/add/<int:company_id>/',
         add_to_watchlist, name='add_to_watchlist'),
    path('companies/remove/<int:company_id>/',
         remove_from_watchlist, name='remove_from_watchlist'),

    # Auth routes
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('google-login/', google_login_view, name='google_login'),
    path('google-login-callback/', google_login_callback,
         name='google_login_callback'),
]
