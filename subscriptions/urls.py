"""
URL configuration for subscriptions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from plans import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from plans.api.views import PlanViewSet  # type: ignore # Adjust the import path as necessary

router = DefaultRouter()
router.register(r'plans', PlanViewSet)  # Register the PlanViewSet with the router

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin path


    # Include other apps' URLs as needed...
]


schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)







urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', views.home, name='home'),
    path('plans/<int:pk>', views.plan, name='plan'),
    path('', include('plans.urls')),  # Include non-API routes from the plans app
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/signup', views.SignUp.as_view(), name='signup'),
    path('join', views.join, name='join'),
    path('checkout', views.checkout, name='checkout'),
    path('auth/settings', views.settings, name='settings'),
    path('updateaccounts', views.updateaccounts, name='updateaccounts'),


#api's
     path('api/', include(router.urls)),  # Include the API routes




]
