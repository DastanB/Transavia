from django.test import TestCase

import xml.etree.ElementTree as ET

from .services import fetch_countries, fetch_cities, fetch_airports, save_countries, save_cities, save_airports

# Create your tests here.
class ServiceTestCase(TestCase):
    def test_fetch_countries(self):
        countries = fetch_countries()
        self.assertGreater(len(countries), 0)
        self.assertIsInstance(countries, ET.Element)
    
    def test_fetch_cities(self):
        cities = fetch_cities()
        self.assertGreater(len(cities), 0)
        self.assertIsInstance(cities, ET.Element)
    
    def test_fetch_airports(self):
        airports = fetch_airports()
        self.assertGreater(len(airports), 0)
        self.assertIsInstance(airports, ET.Element)
    
    def test_save_countries(self):
        ctrs = [{"code": "AD", "name": "Andorra", "continent": "Sw Europe"},
                {"code": "AE", "name": "United Arab Emirates", "continent": "Middle East"}]
        countries = ET.Element("Countries")

        for ctr in ctrs:
            country = ET.Element("Country")
            countries.append(country)
            code = ET.SubElement(country, "CountryCode")
            code.text = ctr["code"]
            name = ET.SubElement(country, "CountryName")
            name.text = ctr["name"]
            continent = ET.SubElement(country, "Continent")
            continent.text = ctr["continent"]
        
        cntrs = ET.Element("Countries") # Empty XML of Countries
        empty_countries = []

        self.assertEqual(save_countries(countries), True)
        self.assertEqual(save_countries(cntrs), False)
        self.assertEqual(save_countries(empty_countries), False)
    
    def test_save_cities(self):
        ctys = [{"code": "WGB", "name": "Bahawalnagar", "state_code": "", "country_code": "PK"},
                {"code": "JER", "name": "Jersey", "state_code": "", "country_code": "GB"}]
        
        cities = ET.Element("Cities")

        for cty in ctys:
            city = ET.Element("Country")
            cities.append(city)
            code = ET.SubElement(city, "CityCode")
            code.text = cty["code"]
            name = ET.SubElement(city, "CityName")
            name.text = cty["name"]
            state_code = ET.SubElement(city, "StateCode")
            state_code.text = cty["state_code"]
            country_code = ET.SubElement(city, "CountryCode")
            country_code.text = cty["country_code"]
        
        cits = ET.Element("Cities") # Empty XML of Cities
        empty_cities = []

        self.assertEqual(save_cities(cities), True)
        self.assertEqual(save_cities(cits), False)
        self.assertEqual(save_cities(empty_cities), False)
    
    def test_save_airports(self):
        ports = [{"code": "WNP", "name": "Naga", "country_code": "PH", "city_code": "WNP", "type_code": "A"},
                {"code": "BCU", "name": "Bauchi", "country_code": "NG", "city_code": "BCU", "type_code": "A"}]

        airports = ET.Element("Airports")

        for port in ports:
            airport = ET.Element('Airport')
            airports.append(airport)
            code = ET.SubElement(airport, "AirportCode")
            code.text = port["code"]
            name = ET.SubElement(airport, "AirportName")
            name.text = port["name"]
            country_code = ET.SubElement(airport, "CountryCode")
            country_code.text = port["country_code"]
            city_code = ET.SubElement(airport, "CityCode")
            city_code.text = port["city_code"]
            type_code = ET.SubElement(airport, "TypeCode")
            type_code.text = port["type_code"]
        
        air_ports = ET.Element("Airports")  # Empty XML of Airports
        emprt_airports = []

        self.assertEqual(save_airports(airports), True)
        self.assertEqual(save_airports(air_ports), False)
        self.assertEqual(save_airports(emprt_airports), False)