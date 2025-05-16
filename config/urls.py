"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from companies.views import CompanyViewSet
from watchlist.views import WatchlistViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Traders Portal API",
        default_version='v1',
        description="API documentation for Traders Portal",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# API routers
router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company-api')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist-api')

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),

    # SSR routes (HTML) only in core.urls
    path('', include('core.urls')),

    # API documentation
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
