from functools import reduce

from django.conf import settings
from django.core.cache import cache


class CacheService:
    @classmethod
    def generate_cache_key(cls, key, complementary_keys, **kwargs):
        cache_key = key

        cache_key = (
            reduce(
                lambda acc, c_key: "{0}_{1}".format(acc, kwargs[c_key]),
                complementary_keys,
                cache_key,
            )
            .replace(" ", "_")
            .replace(",", "_")
        )

        return cache_key

    @classmethod
    def get_cache(cls, cache_id):
        try:
            return cache.get(cache_id)
        except Exception:
            return None

    @classmethod
    def set_cache(cls, cache_id, value, cache_ttl=settings.CACHE_TTL):
        cache.delete(cache_id)
        cache.set(cache_id, value, cache_ttl)
