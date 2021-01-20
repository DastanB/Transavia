from django.urls import path, include

from rest_framework import routers

from .views import store, CountryViewSet, CityViewSet, AirportViewSet

router = routers.DefaultRouter()
router.register('countries', CountryViewSet, basename='countries')
router.register('cities', CityViewSet, basename='cities')
router.register('airports', AirportViewSet, basename='airports')

urlpatterns = [
    path('store/', store),
] + router.urls

