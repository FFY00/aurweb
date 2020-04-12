import http.client
import urllib.parse


class WsgiHttpProxy:
    """
    WSGI-to-HTTP proxy, that is to say a WSGI application that forwards every
    WSGI request to an HTTP server, then the HTTP response back to WSGI.

    The base URL the constructor takes is something like
    `http://localhost:8080`. It must not contain a path, a query string or a
    fragment, as the proxy wouldn’t now what to do with it.

    Only the HTTP scheme is supported, but HTTPS could probably be easily added.
    """

    def __init__(self, base_url):
        parts = urllib.parse.urlsplit(base_url)
        self.netloc = parts.netloc
        # Limitations of this dumb proxy
        assert parts.scheme == "http"
        assert parts.path in ("", "/")
        assert parts.query == ""
        assert parts.fragment == ""

    def __call__(self, environ, start_response):
        conn = http.client.HTTPConnection(self.netloc)
        conn.request(
            method=environ["REQUEST_METHOD"],
            url=urllib.parse.urlunsplit((
                "http", self.netloc,
                urllib.parse.quote(environ["PATH_INFO"]),
                environ["QUERY_STRING"], "")),
            body=environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0))),
        )
        resp = conn.getresponse()
        start_response(f"{resp.status} {resp.reason}", resp.getheaders())
        return resp
