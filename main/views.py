from django.shortcuts import render
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

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
from .serializers import CountryDetailedSerializer, CityDetailedSerializer, AirportSerializer, SearchSerializer
from .services import store_countries, store_cities, store_airports, search_cities
from .constants import CACHE_TTL

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
        """This action returns result of a search request using cache"""
        paginator = LimitOffsetPagination()
        paginator.page_size = 20

        data = request.data
        search_serializer = SearchSerializer(data=data)

        if search_serializer.is_valid(raise_exception=True):
            code = search_serializer.validated_data['code'].lower()
            if code in cache:
                result = cache.get(code)
                return Response(result)
            else: 
                cities, all_cities = search_cities(code)
                page = paginator.paginate_queryset(all_cities, request)

                serializer = CityDetailedSerializer(page, many=True, context = {"code": code, "cities": cities})
                result = serializer.data
                cache.set(code, result, timeout=CACHE_TTL)

                return paginator.get_paginated_response(result)

class AirportViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """This viewset returns list of airports"""
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer