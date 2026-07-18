from ninja.security import APIKeyHeader

from .models.api_key import ApiKey

API_KEY_HEADER = "apikey"


class ApiKeyAuth(APIKeyHeader):
    param_name = API_KEY_HEADER

    def authenticate(self, request, key):
        return ApiKey.authenticate(key)
