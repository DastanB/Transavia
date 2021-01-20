import requests
import logging
import xml.etree.ElementTree as ET

from .models import Country, City, Airport
from .constants import COUNTRY_URL, CITY_URL, AIRPORT_URL, TIMEOUT

logger = logging.getLogger(__name__)

def fetch_countries():
    countries = []

    try:
        response = requests.get(
            COUNTRY_URL,
            timeout=TIMEOUT
        )    
        countries = ET.fromstring(response.content)
        logger.info(f"Countries were fetched")
            
    except Exception as e:
        logger.info(f"{e}")

    return countries

def save_countries(countries):
    status = False
    if len(countries) > 0 and isinstance(countries, ET.Element):
        for country in countries:
            ctr = Country.objects.get_or_create(
                code = country.find('CountryCode').text if country.find('CountryCode') is not None else "",
                name = country.find('CountryName').text if country.find('CountryName') is not None else "",
                continent = country.find('Continent').text if country.find('Continent') is not None else ""
            )
            if isinstance(ctr[0], Country): 
                status = True
            if ctr[1]:
                logger.info(f"{ctr[0].name} was created")
    
    return status    

def store_countries():
    countries = fetch_countries()
    return save_countries(countries)

def fetch_cities():
    cities = []

    try:
        response = requests.get(
            CITY_URL,
            timeout=TIMEOUT
        )    
        cities = ET.fromstring(response.content)
        logger.info(f"Cities were fetched")
            
    except Exception as e:
        logger.info(f"{e}")

    return cities

def save_cities(cities):
    status = False
    if len(cities) > 0:
        for city in cities:
            cty = City.objects.get_or_create(
                code = city.find('CityCode').text if city.find('CityCode') is not None else "",
                name = city.find('CityName').text if city.find('CityName') is not None else "",
                state_code = city.find('StateCode').text if city.find('StateCode') is not None else "",
                country_code = city.find('CountryCode').text if city.find('CountryCode') is not None else ""
            )
            if isinstance(cty[0], City):
                status = True
            if cty[1]:
                logger.info(f"{cty[0].name} was created")

    return status

def store_cities():
    cities = fetch_cities()
    return save_cities(cities)

def fetch_airports():
    airports = []

    try:
        response = requests.get(
            AIRPORT_URL,
            timeout=TIMEOUT
        )    
        airports = ET.fromstring(response.content)
        logger.info(f"Airports were fetched")
            
    except Exception as e:
        logger.info(f"{e}")

    return airports

def save_airports(airports):
    status = False

    if len(airports) > 0:
        for airport in airports:
            port = Airport.objects.get_or_create(
                code = airport.find('AirportCode').text if airport.find('AirportCode') is not None else "",
                name = airport.find('AirportName').text if airport.find('AirportName') is not None else "",
                country_code = airport.find('CountryCode').text if airport.find('CountryCode') is not None else "",
                city_code = airport.find('CityCode').text if airport.find('CityCode') is not None else "",
                type_code = airport.find('TypeCode').text if airport.find('TypeCode') is not None else ""
            )
            if isinstance(port[0], Airport):
                status = True
            if port[1]:
                logger.info(f"{port[0].name} was created")
    
    return status

def store_airports():
    airports = fetch_airports()
    return save_airports(airports)

def search_cities(code):
    cities_by_code = City.objects.filter(code__icontains=code)
    cities_by_name = City.objects.filter(name__icontains=code)
    cities_by_country_code = City.objects.filter(country_code__icontains=code)
    cities_by_state_code = City.objects.filter(state_code__icontains=code)
    cities = (cities_by_code | cities_by_name | cities_by_country_code | cities_by_state_code).distinct().all()
    
    airports = Airport.objects.filter(code__icontains=code)
    cities_by_airport = City.objects.filter(code__in=airports.values_list('city_code', flat=True).distinct())

    all_cities = cities.union(cities_by_airport).distinct()

    return cities, all_cities
