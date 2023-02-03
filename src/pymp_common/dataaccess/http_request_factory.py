from typing import Mapping
from typing_extensions import TypeAlias
from requests import Request

_HeadersMapping: TypeAlias = Mapping[str, str or bytes]


class HttpRequestFactory():

    def get(self, base_url: str, path: str, headers: _HeadersMapping = {}) -> Request:
        return Request(
            method='GET',
            url=f"{base_url}{path}",
            headers=headers
        )

    def post(self, base_url: str, path: str, data, headers = {}) -> Request:        
        headers['Content-Type'] = 'application/json'
        return Request(
            method='POST',
            url=f"{base_url}{path}",
            headers=headers,
            json=data
        )

    def post_data(self, base_url: str, path: str, data, headers: _HeadersMapping = {}) -> Request:
        return Request(
            method='POST',
            url=f"{base_url}{path}",
            headers=headers,
            data=data
        )


http_request_factory = HttpRequestFactory()
