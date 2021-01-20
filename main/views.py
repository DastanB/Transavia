from django.shortcuts import render

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend

from .models import Country, City, Airport
from .serializers import CountryDetailedSerializer, CityDetailedSerializer, AirportSerializer
from .services import store_countries, store_cities, store_airports

import requests
import logging
import xml.etree.ElementTree as ET
import itertools

# Create your views here.
@api_view(['GET'])
def store(request):
    """This view stores all countries, cities and airports."""
    stored_countries = store_countries()
    stored_cities = store_cities()
    stored_airports = store_airports()
    
    return Response({"countries_stored": stored_countries,
                    "cities_stored": stored_cities,
                    "airports_stored": stored_airports})

class CountryViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """This viewset returns list of countries"""
    queryset = Country.objects.all()
    serializer_class = CountryDetailedSerializer

class CityViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """This viewset returns list of cities"""
    queryset = City.objects.all()
    serializer_class = CityDetailedSerializer

    @action(methods=['POST'], detail=False)
    def search(self, request):
        paginator = LimitOffsetPagination()
        paginator.page_size = 20

        data = request.data
        code = data['code']

        cities_by_code = City.objects.filter(code__icontains=code)
        cities_by_name = City.objects.filter(name__icontains=code)
        cities_by_country_code = City.objects.filter(country_code__icontains=code)
        cities_by_state_code = City.objects.filter(state_code__icontains=code)
        cities = (cities_by_code | cities_by_name | cities_by_country_code | cities_by_state_code).distinct().all()
        
        airports = Airport.objects.filter(code__icontains=code)
        cities_by_airport = City.objects.filter(code__in=airports.values_list('city_code', flat=True).distinct())

        all_cities = cities.union(cities_by_airport).distinct()
        page = paginator.paginate_queryset(all_cities, request)

        serializer = CityDetailedSerializer(page, many=True, context = {"code": code, "cities": cities})

        return paginator.get_paginated_response(serializer.data)

class AirportViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """This viewset returns list of airports"""
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer