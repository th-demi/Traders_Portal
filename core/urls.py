from django.urls import path
from .views import (
    home_view, company_list_view, watchlist_view,
    add_to_watchlist, remove_from_watchlist,
    login_view, register_view, logout_view,
    google_login_view, google_login_callback
)

urlpatterns = [
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
