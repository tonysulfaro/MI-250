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
            self.wfile.write(b'''2. The service will offer the following end-points:

    -   GET /albums   #Gets all albums that the your system has local knowledge of
                      #HTML page renders as a table in a browser
                      #Should support the use of query parameters to search for any fields in the album

    -   GET /albums/{id}            #Gets the album, with complete track listing

    -   GET /albums/query/{id}      #Gets a list of albums returned by a query (see the POST below)
                                    #This url will timeout after 1 hour

    -   GET /users/{id}/            #Gets all user info, including id's of albums, playlists
    -   GET /users/{id}/albums      #Just lists the user's albums
    -   GET /users/{id}/playlists   #Just lists the user's playlists


    -   GET /users                  #Gets all users

    -   GET /playlists              #Gets all playlists
    -   GET /playlists/{id}         #Gets specific playlist, with list of track names / length
    -   GET /playlists/query/{id}   #Gets a list of playlists returned by a query (see the POST below)
                                    #This url will timeout after 1 hour

    -   DELETE /users/{id}      #Only successful if a user deletes themselves
    -   DELETE /playlists/{id}  #Only successful if no users "own" the playlist
    -   DELETE /albums/{id}     #Only successful if no users "own" the id

    -   PUT|DELETE /playlists/{id}          #Adds/Deletes a favorite album to the user's list of fav
                                            #Authenticated
    -   PUT /playlists/query/{id}/{idx}     #Saves the query result to the user's playlists
                                            #Requires a query parameter to name the playlist

    -   PUT|DELETE /albums/{id}         #Adds/Deletes a favorite playlist to the user's list of favs
                                        #Authenticated
    -   PUT /

    -   POST /albums    #Post a body as a form with fields corresponding to the fields in an album
                        #You will search your backend service (spotify / discogs) and redirect the user
                        #To a unique query url with all of the matching albums

    -   POST /playlists     #Authenticated post with an empty body creates a playlist based on the user's
                            #favorite albums
                            #Post with a body containing an album id creates a playlist based on that album
                            #Must be an id that the system knows about, or return an error
                            #Unauthenticated posts requre a body
                            #In all cases, redirects the user to a unique query url

    -   POST /users/{id}/token      #Returns a token (nonce) that the user can use to access the service
                                    #Requires username & password parameters
                                    #Token should expire after 10 minutes of inactivity

    -   POST /users         #Create a new user.  Requires a username and password as form parameters
                            #Fails is username is taken & password does not match
                            #Success redirects to the pre-existing or newly created /users/{id}

3.  All urls that return something should handle text/json.  The following should also render html with the appropriate content header

    -   GET /albums                 # Should contain basic info, and link to album for track listing
    -   GET /playlists              # Should contain titles, with links to each playlist for track listing
    -   GET /albums/{id}            # Album with track listing
    -   GET /playlists/{id}         # Playlist with track listing
    -   GET /users/{id}/playlists   # As above
    -   GET /users/{id}/albums      # As above
''')

        elif path_list[1] == 'albums':

            fp = open('./data/albums.json', 'r')
            data = json.load(fp)

            if len(path_list) == 2:  # getting all album data

                self.send_response(200)
                self.end_headers()
                send = json.dumps(data)
                self.wfile.write(send.encode())

            if len(path_list) == 3:  # getting album by id

                if path_list[2].isdigit():  # id

                    self.send_response(200)
                    self.end_headers()
                    position = int(path_list[2])
                    self.wfile.write(get_item_by_key(data, position))

        elif path_list[1] == 'users':

            fp = open('./data/users.json', 'r')
            data = json.load(fp)

            if len(path_list) == 2:  # get all user data /users

                self.send_response(200)
                self.end_headers()
                send = json.dumps(data)
                self.wfile.write(send.encode())

            elif len(path_list) == 3:  # get user data by user id /users/{id}

                if path_list[2].isdigit():  # only getting data by id /users/{id}
                    self.send_response(200)
                    self.end_headers()
                    position = int(path_list[2])
                    self.wfile.write(get_item_by_key(data, position))

            elif len(path_list) == 4:

                if path_list[3] == 'albums':
                    self.send_response(200)
                    self.end_headers()
                    position = int(path_list[2])
                    self.wfile.write(get_item_by_key(data, position, 'albums'))

                elif path_list[3] == 'playlists':
                    self.send_response(200)
                    self.end_headers()
                    position = int(path_list[2])
                    self.wfile.write(get_item_by_key(data, position, 'playlists'))

        elif path_list[1] == 'playlists':

            fp = open('./data/albums.json', 'r')
            data = json.load(fp)

            if len(path_list) == 2:  # get all playlist data
                self.send_response(200)
                self.end_headers()
                send = json.dumps(data)
                self.wfile.write(send.encode())

            elif len(path_list) == 3:  # get playlist by id
                self.send_response(200)
                self.end_headers()
                position = int(path_list[2])
                self.wfile.write(get_item_by_key(data, position))

            elif len(path_list) == 4:
                self.send_response(200)
                self.end_headers()
                position = int(path_list[2])
                self.wfile.write(get_item_by_key(data, position))  # GET /playlists/query/{id}

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


def get_item_by_key(data, item_id, json_key=-1):

    for item in data:
        for key, value in item.items():
            if key == 'id' and value == item_id:
                if json_key == -1:
                    json_resp = json.dumps(item)
                else:
                    json_resp = json.dumps(item[json_key])
                return json_resp.encode()


listen_port = 8000
httpd = HTTPServer(('localhost', listen_port), SimpleHTTPRequestHandler)
print('now listening on port:' + str(listen_port))
httpd.serve_forever()
