
import requests


class LoggingRequest(requests.Request):
    def __init__(self, method, url, **kwargs):
        super().__init__(method, url, **kwargs)
        self.log = []

    def log_request(self, response):
        log_message = f"{self.method} request to {self.url} returned with status code {response.status_code}"
        self.log.append(log_message)
        print(log_message)


class LoggingSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.log = []

    def request(self, method, url, **kwargs):
        req = LoggingRequest(method, url, **kwargs)
        prepped = self.prepare_request(req)
        resp = self.send(prepped, **kwargs)
        self.log.append(req.log[0])
        return resp


class HttpRequestFactory():

    def get(self, base_url: str, path: str, headers={}) -> requests.Request:
        return LoggingRequest(
            method='GET',
            url=f"{base_url}{path}",
            headers=headers,
            timeout=(3.05, 30)
        )

    def post_json(self, base_url: str, path: str, data, headers={}) -> requests.Request:
        headers['Content-Type'] = 'application/json'
        return LoggingRequest(
            method='POST',
            url=f"{base_url}{path}",
            headers=headers,
            json=data,
            timeout=(3.05, 30)
        )

    def post_data(self, base_url: str, path: str, data, headers={}) -> requests.Request:
        return LoggingRequest(
            method='POST',
            url=f"{base_url}{path}",
            headers=headers,
            data=data,
            timeout=(3.05, 30)
        )


http_request_factory = HttpRequestFactory()
