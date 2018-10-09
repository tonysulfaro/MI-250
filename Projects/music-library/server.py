"""
Module 04 Project - Music Library
Tony Sulfaro
MI 250.001
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from io import BytesIO
import secrets
from datetime import *


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

                send_resp_GET(self, data)

            if len(path_list) == 3:  # getting album by id

                if path_list[2].isdigit():  # id
                    album_id = int(path_list[2])
                    send_resp_GET(self, data, album_id, 'id')

        elif path_list[1] == 'users':

            fp = open('./data/users.json', 'r')
            data = json.load(fp)

            if len(path_list) == 2:  # get all user data /users

                send_resp_GET(self, data)

            elif len(path_list) == 3:  # get user data by user id /users/{id}

                if path_list[2].isdigit():  # only getting data by id /users/{id}

                    user_id = int(path_list[2])
                    send_resp_GET(self, data, user_id, 'id')

            elif len(path_list) == 4:  # get user albums

                user_id = int(path_list[2])

                if path_list[3] == 'albums':  # get user albums
                    send_resp_GET(self, data, user_id, 'id', 'albums')

                elif path_list[3] == 'playlists':  # get user playlists
                    send_resp_GET(self, data, user_id, 'id', 'playlists')

        elif path_list[1] == 'playlists':

            fp = open('./data/albums.json', 'r')
            data = json.load(fp)

            if len(path_list) == 2:  # get all playlist data
                send_resp_GET(self, data)

            elif len(path_list) == 3:  # get playlist by id
                playlist_id = int(path_list[2])
                send_resp_GET(self, data, playlist_id, 'id')

            elif len(path_list) == 4:
                self.send_response(200)
                self.end_headers()
                position = int(path_list[2])
                self.wfile.write(get_item_from_json(data, position, 'id'))  # GET /playlists/query/{id}

        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        path_list = self.path.split('/')
        print(path_list)

        token_begin = path_list[2].find('token=')
        token = path_list[2][token_begin + len('token='):]

        data_type = path_list[1]
        json_id = path_list[2][:token_begin - 1]

        if validate_token(token):
            self.send_response(200)
            self.end_headers()
            delete_item_from_json(data_type, int(json_id))
        else:
            self.send_response(401)
            self.end_headers()

    def do_PUT(self):
        pass

    def do_POST(self):
        path_list = self.path.split('/')
        print(path_list)

        if len(path_list) == 2:  # create a new user
            user_id = create_user(path_list)
            if user_id != -1:
                self.send_response(301)
                self.send_header('New User', 'http://localhost:8000/users/' + str(user_id))
                self.end_headers()
            else:
                self.send_response(405)
                self.end_headers()

        elif len(path_list) == 3:
            pass
        elif len(path_list) == 4:  # get token by posting to users

            if path_list[1] == 'users' and 'token' in path_list[3]:

                user_name, password = get_user_pass(path_list)

                if validate_credentials(user_name, password):
                    token = generate_token(user_name)

                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(token.encode())
                else:
                    self.send_response(401)
                    self.end_headers()

        else:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            self.send_response(404)
            self.end_headers()
            response = BytesIO()
            response.write(b'This is POST request. ')
            response.write(b'Received: ')
            response.write(body)
            self.wfile.write(response.getvalue())


def send_resp_GET(self, data, item_id=-1, json_key=-1, json_data_type=''):

    if json_key == -1 and item_id == -1:
        self.send_response(200)
        self.end_headers()
        send = json.dumps(data)
        self.wfile.write(send.encode())
        return

    if json_data_type != '':
        send = get_item_from_json(data, item_id, json_key, json_data_type)
    else:
        send = get_item_from_json(data, item_id, json_key)
    if send is None:
        self.send_response(404)
        self.end_headers()
    else:
        self.send_response(200)
        self.end_headers()
        self.wfile.write(send)


def get_item_from_json(data, item_id, json_obj_key, json_key=-1):
    for item in data:
        if item[json_obj_key] == item_id:
            if json_key == -1:
                json_resp = json.dumps(item)
            else:
                json_resp = json.dumps(item[json_key])
            return json_resp.encode()


def delete_item_from_json(operation, item_id):
    if operation == 'users':
        fp = open('./data/users.json', 'r')
        data = json.load(fp)
        new_data = []

        for item in data:
            if item['id'] != int(item_id):
                new_data.append(item)

        new_json = json.dumps(new_data)
        fp_new = open('./data/users.json', 'w', encoding='UTF-8')
        fp_new.write(new_json)

    elif operation == 'playlists':
        fp = open('./data/playlists.json', 'r')
        data = json.load(fp)
        new_data = []

        for item in data:
            if item['id'] != int(item_id):
                new_data.append(item)

        new_json = json.dumps(new_data)
        fp_new = open('./data/playlists.json', 'w', encoding='UTF-8')
        fp_new.write(new_json)

    elif operation == 'albums':
        fp = open('./data/albums.json', 'r')
        data = json.load(fp)
        new_data = []

        for item in data:
            if item['id'] != int(item_id):
                new_data.append(item)

        new_json = json.dumps(new_data)
        fp_new = open('./data/albums.json', 'w', encoding='UTF-8')
        fp_new.write(new_json)


def create_user(path_list):
    user_name, password = get_user_pass(path_list)
    print('create user')
    print(user_name)
    fp = open('./data/users.json', 'r')
    data = json.load(fp)
    new_data = []

    max_id = 0
    for item in data:
        if item['id'] > max_id:
            max_id = item['id']
        if item['user_name'] == user_name:
            print(item['user_name'])
            return -1

    for item in data:
        new_data.append(item)

    new_data.append({
        "id": max_id + 1,
        "user_name": user_name,
        "albums": [],
        "playlists": []})

    new_json = json.dumps(new_data)
    fp_new = open('./data/users.json', 'w', encoding='UTF-8')
    fp_new.write(new_json)
    return max_id + 1


def get_user_pass(path_list):
    user_name = ''
    password = ''

    if len(path_list) == 2:
        user_name_index = path_list[1].find('user_name=') + len('user_name=')
        and_index = path_list[1].find('&', user_name_index)
        password_index = path_list[1].find('password=', and_index) + len('password=')

        user_name = path_list[1][user_name_index:and_index]
        password = path_list[1][password_index:]

    elif len(path_list) == 4:
        user_name_index = path_list[3].find('user_name=') + len('user_name=')
        and_index = path_list[3].find('&', user_name_index)
        password_index = path_list[3].find('password=', and_index) + len('password=')

        user_name = path_list[3][user_name_index:and_index]
        password = path_list[3][password_index:]

    return user_name, password


def validate_credentials(username, password):
    fp = open('./data/logins.csv', 'r')

    for line in fp:
        line = line.split(',')
        if line[0] == username and line[1] == password:
            return True
    return False


def generate_token(user_name):
    token = secrets.token_urlsafe()

    fp = open('./data/tokens.csv', 'a')
    exp_time = datetime.now() + timedelta(minutes=10)

    fp.write(user_name + ',' + token + ',' + str(exp_time) + '\n')

    return token


def validate_token(token):
    fp = open('./data/tokens.csv', 'r')

    for line in fp:
        line = line.strip().split(',')

        if line[1] == token:
            if str(datetime.now()) <= line[2]:
                update_token_time(line[2])
                return True
    return False


def update_token_time(timestamp):
    readfile = open('./data/tokens.csv', 'r')
    file_data = readfile.read()

    exp_time = datetime.now() + timedelta(minutes=10)
    file_data = file_data.replace(str(timestamp), str(exp_time))

    readfile.close()

    # write string to file
    outfile = open('./data/tokens.csv', 'w')
    outfile.write(file_data)
    outfile.close()


listen_port = 8000
httpd = HTTPServer(('localhost', listen_port), SimpleHTTPRequestHandler)
print('now listening on port:' + str(listen_port))
httpd.serve_forever()
