from abc import ABC, abstractmethod

from ..domain.api_key import ApiKey


class ApiKeyStore(ABC):
    @abstractmethod
    def save(self, api_key: ApiKey) -> ApiKey:
        raise NotImplementedError
