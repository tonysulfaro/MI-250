"""
Module 04 Project - Music Library
Tony Sulfaro
MI 250.001
"""
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'main page')

        elif self.path == '/albums':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'albums')

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'404 resource not found')

    def do_POST(self):
        print(self.request)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'posty')


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()