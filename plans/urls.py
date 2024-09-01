from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('', views.home, name='home'),
    path('plan/<int:pk>/', views.plan, name='plan'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('join/', views.join, name='join'),
    path('checkout/', views.checkout, name='checkout'),
    path('settings/', views.settings, name='settings'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('updateaccounts/', views.updateaccounts, name='updateaccounts'),

#apis urls


]