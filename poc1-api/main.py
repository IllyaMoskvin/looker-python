from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class SecretSauceMaker:
    """
    Substitute this for an ML model, optimization function, etc.
    """
    def make_sauce(self, foo, bar):
        # TODO: Seeded random number generator here
        # Should output tabular data: maybe date, revenue?
        pass


class SauceSaver():
    """
    Save tabular results to wherever Looker's lookin' at
    """
    def save_sauce(self):
        # TODO: Save to BigQuery. See this thread:
        # https://discord.com/channels/1163767159466504245/1181709334271496323/1181710892178608209
        pass


class HTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Use your favorite Python API here! Flask, FastAPI, etc.
    We used Python's built-in HTTP for simplicity.
    """
    protocol_version = 'HTTP/1.1'

    def __init__(self, *args, **kwargs):
        # Avoid instantiating the model for each request
        self.sauce_maker = SecretSauceMaker()
        self.sauce_saver = SauceSaver()
        super().__init__(*args, **kwargs)


    def respond(self, code, message):
        # End body with trailing \n to avoid delays:
        body = str(message) + '\n'

        self.send_response(code)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()

        self.wfile.write(str.encode(body))


    def do_GET(self):
        # Parse query string, keep first value for each key
        params = parse_qs(urlparse(self.path).query)
        params = {k: v[0] for k, v in params.items()}

        try:
            # Safer to be explicit about which params to pass
            sauce = self.sauce_maker.make_sauce(
                foo=params.get("foo", 0),
                bar=params.get("bar", 0),
            )
        except Exception:
            return self.respond(500, "Failed to make sauce")

        return self.respond(200, "Made sauce")


def serve(handler):
    # https://stackoverflow.com/questions/43146298/http-request-from-chrome-hangs-python-webserver
    httpd = ThreadingHTTPServer(('', 80), handler)
    httpd.serve_forever()


if __name__ == "__main__":
    serve(HTTPRequestHandler)
