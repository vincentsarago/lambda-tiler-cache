"""Test lambda-tiler locally."""

import click
import base64

from socketserver import ThreadingMixIn

from urllib.parse import urlparse, parse_qsl
from http.server import HTTPServer, BaseHTTPRequestHandler

from lambda_tiler_cache.handler import app


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    """MultiThread."""

    pass


class Handler(BaseHTTPRequestHandler):
    """Requests handler."""

    def do_GET(self):
        """Get requests."""
        q = urlparse(self.path)
        request = {
            "headers": dict(self.headers),
            "path": q.path,
            "queryStringParameters": dict(parse_qsl(q.query)),
            "httpMethod": self.command,
        }
        response = app(request, None)

        self.send_response(int(response["statusCode"]))
        for r in response["headers"]:
            self.send_header(r, response["headers"][r])
        self.end_headers()

        if response.get("isBase64Encoded"):
            response["body"] = base64.b64decode(response["body"])

        if isinstance(response["body"], str):
            self.wfile.write(bytes(response["body"], "utf-8"))
        else:
            self.wfile.write(response["body"])

    def do_POST(self):
        """POST requests."""
        q = urlparse(self.path)
        body = self.rfile.read(int(dict(self.headers).get("Content-Length")))
        body = base64.b64encode(body).decode()
        request = {
            "headers": dict(self.headers),
            "path": q.path,
            "queryStringParameters": dict(parse_qsl(q.query)),
            "body": body,
            "httpMethod": self.command,
        }

        response = app(request, None)

        self.send_response(int(response["statusCode"]))
        for r in response["headers"]:
            self.send_header(r, response["headers"][r])
        self.end_headers()
        if isinstance(response["body"], str):
            self.wfile.write(bytes(response["body"], "utf-8"))
        else:
            self.wfile.write(response["body"])


@click.command(short_help="Local Server")
@click.option("--address", "-l", type=str, default="127.0.0.1", help="localhost")
@click.option("--port", type=int, default=8000, help="port")
def run(address, port):
    """Launch server."""
    server_address = (address, port)
    httpd = ThreadingSimpleServer(server_address, Handler)
    click.echo(f"Starting local server at http://{address}:{port}", err=True)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
