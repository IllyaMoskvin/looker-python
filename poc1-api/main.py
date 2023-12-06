import json
import os
import random

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import psycopg2


class SecretSauceMaker:
    """
    Substitute this for an ML model, optimization function, etc.
    """
    def make_sauce(self, foo, bar):
        dates = [f'2024-{i:02d}-01' for i in range(1, 12)]
        revenue = 1000000
        out = []
        for date in dates:
            seed = date + str(foo) + str(bar)
            random.seed(seed)
            revenue += random.randrange(0, 100000)
            out.append((int(foo), bar, date, revenue))
        return out


class SauceSaver():
    """
    Save tabular results to wherever Looker's lookin' at
    """
    def __init__(self, *args, **kwargs):
        self.connection = psycopg2.connect(
            host=os.environ["DB_HOST"],
            port=int(os.environ["DB_PORT"]),
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            dbname=os.environ["DB_DB"],
        )

    def save_sauce(self, sauce):
        """
        Our sauce maker is deterministic, so we don't need to replace results,
        but we do so here for demonstration.
        """
        pattern = ", ".join(["(%s, %s, %s, %s)" for i in range(len(sauce))])
        values = (sauce[0][0], sauce[0][1]) + sum(sauce, ())
        sql = f"""
            DELETE FROM poc1
            WHERE
                foo = %s AND bar = %s;
            INSERT INTO poc1
                (foo, bar, date, revenue)
            VALUES
                {pattern};
        """

        with self.connection.cursor() as cursor:
            cursor.execute(sql, values)
            self.connection.commit()


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
                bar=params.get("bar", "A"),
            )

            self.sauce_saver.save_sauce(sauce)
        except Exception:
            return self.respond(500, "Failed to make sauce")

        # Uncomment for debug. This API does not return the result.
        # It writes the result to a database connected to Looker.
        # return self.respond(200, json.dumps(sauce))

        return self.respond(200, "Made sauce. Please rerun your query.")


def serve(handler):
    # https://stackoverflow.com/questions/43146298/http-request-from-chrome-hangs-python-webserver
    httpd = ThreadingHTTPServer(('', 80), handler)
    httpd.serve_forever()


if __name__ == "__main__":
    serve(HTTPRequestHandler)
