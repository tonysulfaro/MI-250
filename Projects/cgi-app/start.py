from http.server import CGIHTTPRequestHandler, HTTPServer


def runCgi():

    print('starting server...')

    # Server settings
    server_address = ('127.0.0.1', 8989)
    handler = CGIHTTPRequestHandler

    # I can configure the directories I want to use here
    handler.cgi_directories = ['/cgi']
    httpd = HTTPServer(server_address, handler)
    print('running server...')
    print('now listening on port: ' + str(server_address[1]))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


def main():
    runCgi()


if __name__ == "__main__":
    main()
