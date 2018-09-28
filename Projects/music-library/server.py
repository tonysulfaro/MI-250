"""
Module 04 Project - Music Library
Tony Sulfaro
MI 250.001
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from io import BytesIO


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        path_list = self.path.split('/')
        print(path_list)

        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'main page')

        elif self.path == '/albums':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'albums')

        elif path_list[1] == 'users':
            if path_list[3] == 'albums':
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'hmmm')
            elif path_list[3] == 'playlists':
                pass
            elif 'playlists' in self.path:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'')

        else:
            json_string = json.dumps(path_list)
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json_string.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()