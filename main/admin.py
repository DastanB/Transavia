from django.contrib import admin

from .models import Country, City, Airport

# Register your models here.
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'continent')
    search_fields = ('name', 'code', 'continent')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'state_code', 'country_code')
    search_fields = ('code', 'name', 'state_code', 'country_code')

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'country_code', 'city_code', 'type_code')
    search_fields = ('code', 'name', 'country_code', 'city_code', 'type_code')