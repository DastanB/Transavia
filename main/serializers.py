from rest_framework import serializers

from .models import Country, City, Airport

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"

class CountryDetailedSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()
    
    class Meta:
        model = Country
        fields = ('id', 'code', 'name', 'continent', 'cities')

    def get_cities(self, obj: Country):    
        cities = City.objects.filter(country_code=obj.code)
        return CitySerializer(cities, many=True).data

class CityDetailedSerializer(serializers.ModelSerializer):
    airports = serializers.SerializerMethodField()
    
    def get_airports(self, obj: City):
        if self.context.get('code') is not None:
            if self.context['code'].lower() not in obj.name.lower() and self.context['code'].lower() not in obj.code.lower():
                return AirportSerializer(Airport.objects.filter(code__icontains=self.context['code']), many=True).data
            
        airports = Airport.objects.filter(city_code=obj.code)
        return AirportSerializer(airports, many=True).data

    class Meta: 
        model = City
        fields = ('id', 'code', 'name', 'state_code', 'country_code', 'airports')

class SearchSerializer(serializers.Serializer):
    code = serializers.CharField()
