import json
import zlib

from django.core.cache import caches
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Country, City, Airport

def cache_object(obj, cache_name, cache_key):
    compressed_all = zlib.compress(json.dumps(obj, separators=(',', ':')).encode('utf-8'), 9)
    caches[cache_name].set(cache_key, compressed_all, timeout=None)


def cache_instance(instance, serializer, serializer_params, cache_name):
    serialized_object = serializer(instance=instance, **serializer_params).data
    cache_object(serialized_object, cache_name, instance.slug)
    return serialized_object