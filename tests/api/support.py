import json


class ApiSession:
    def __init__(self, client, auth: dict | None = None):
        self.client = client
        self.auth = auth or {}

    def get(self, path: str, *, expected: int = 200, **headers):
        return self._request("get", path, expected=expected, headers=headers)

    def post(self, path: str, payload: dict | None = None, *, expected: int = 200, **headers):
        return self._request("post", path, payload, expected=expected, headers=headers)

    def put(self, path: str, payload: dict, *, expected: int = 200, **headers):
        return self._request("put", path, payload, expected=expected, headers=headers)

    def patch(self, path: str, payload: dict, *, expected: int = 200, **headers):
        return self._request("patch", path, payload, expected=expected, headers=headers)

    def delete(self, path: str, *, expected: int = 204, **headers):
        return self._request("delete", path, expected=expected, headers=headers)

    def _request(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
        *,
        expected: int,
        headers: dict,
    ):
        request = getattr(self.client, method)
        kwargs = self.auth | headers
        if payload is not None:
            kwargs.update(data=json.dumps(payload), content_type="application/json")
        response = request(path, **kwargs)
        assert response.status_code == expected, response.content
        return response


class EndpointAssertions:
    def api(self, client, auth: dict | None = None) -> ApiSession:
        return ApiSession(client, auth)
