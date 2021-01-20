from django.db import models

# Create your models here.
class Country(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    continent = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name    

class City(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    state_code = models.CharField(max_length=255, null=True, blank=True)
    country_code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name

class Airport(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255)
    city_code = models.CharField(max_length=255)
    type_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name