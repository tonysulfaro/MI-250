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
import requests


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

        # GET /query
        if 'query' in path_list[1]:

            start_query_type = path_list[1].find('query_type=')
            end_query_type = path_list[1].find('&', start_query_type)
            query_type = path_list[1][start_query_type + len('query_type='):end_query_type]

            start_search = path_list[1].find('search_term=')
            search = path_list[1][start_search + len('search_term='):]

            spotify_token = get_spotify_token()
            query = [query_type, search]

            data = search_spotify(spotify_token, query)
            # data = json.dumps(data)

            page = generate_spotify_page(query_type, data)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(page.encode())

        elif path_list[1] == 'albums':

            fp = open('./data/albums.json', 'r')
            data = json.load(fp)

            if len(path_list) == 2:  # getting all album data

                if path_list[1] == 'albums':
                    # GET /albums
                    print(self.headers)

                    if 'Content-Type' in self.headers:
                        print('yes')

                        if 'json' in self.headers['Content-Type']:
                            send_resp_GET(self, data)
                    else:
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(generate_page_from_json('albums', data).encode())

            if len(path_list) == 3:  # getting album by id

                if path_list[2].isdigit():  # id
                    album_id = int(path_list[2])
                    if 'Content-Type' in self.headers:
                        print('yes')

                        if 'json' in self.headers['Content-Type']:

                            send_resp_GET(self, data, album_id, 'id')
                    else:
                        self.send_response(200)
                        self.end_headers()
                        data = json.loads(get_item_from_json(data, album_id, 'id').decode())
                        self.wfile.write(generate_page_from_json('album', data).encode())

                elif 'query' in path_list:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"""<!DOCTYPE html>
                    <html>
                    <head>
                        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
                    </head>
                    <body>
                    
                    <h2>Spotify Search</h2>
                    
                    <form action="http://localhost:8000/query" method="get">
                        Search Type: 
                        <br>
                        <select name="query_type">
                          <option value="artist">Artist</option>
                          <option value="album">Album</option>
                          <option value="playlist">Playlist</option>
                        </select>
                        <br>
                          Search Term:<br>
                          <input type="text" name="search_term" value="">
                          <br>
                          <input type="submit" value="Submit">
                    </form> 
                    
                    <p>If you click the "Submit" button, the form-data will be submitted then redirected to a results page</p>
                    
                    </body>
                    </html>""")

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

            fp = open('./data/playlists.json', 'r')
            data = json.load(fp)

            # GET /playlists
            if len(path_list) == 2:

                if 'Content-Type' in self.headers:

                    if 'json' in self.headers['Content-Type']:
                        send_resp_GET(self, data)
                else:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(generate_page_from_json('playlists', data).encode())

            # GET /playlists /{id}
            elif len(path_list) == 3:

                playlist_id = int(path_list[2])
                if 'Content-Type' in self.headers:

                    if 'json' in self.headers['Content-Type']:

                        send_resp_GET(self, data, playlist_id, 'id')
                else:
                    self.send_response(200)
                    self.end_headers()
                    data = json.loads(get_item_from_json(data, playlist_id, 'id').decode())
                    print(type(data))
                    self.wfile.write(generate_page_from_json('playlist', data).encode())



            # GET /playlists/query/{id}
            elif len(path_list) == 4:

                form_page = """<!DOCTYPE html>
                                                <html>
                                                <head>
                                                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
                                                </head>
                                                <body>

                                                <h2>Album Search Results</h2>
                                                <h3>Check albums and then click submit to save</h3>

                                                <form action="http://localhost:8000/playlists" method="post">
                                                  """

                form_page += """<input type="checkbox" name="sample" value="artist" /> Artist_name <br>
                                <input type="checkbox" name="sample" value="artist2" /> Another_artist <br>"""

                form_page += """<input type="submit" value="Submit">
                                                </form>

                                                </body>
                                                </html>"""
                self.send_response(200)
                self.end_headers()
                self.wfile.write(form_page.encode())

        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):

        user_fp = open('./data/users.json', 'r', encoding='UTF-8')
        user_data = json.loads(user_fp.read())

        album_fp = open('./data/albums.json', 'r', encoding='UTF-8')
        album_data = json.loads(album_fp.read())

        playlists_fp = open('./data/playlists.json', 'r', encoding='UTF-8')
        playlists_data = json.loads(playlists_fp.read())

        path_list = self.path.split('/')
        print(path_list)

        token_begin = path_list[2].find('token=')
        token = path_list[2][token_begin + len('token='):]

        data_type = path_list[1]
        json_id = int(path_list[2][:token_begin - 1])

        print(json_id)

        if validate_token(token):

            if path_list[1] == 'users':
                # check if user is only doing operation on themselves
                user_name = json.loads(get_item_from_json(user_data, json_id, 'id'))['user_name']
                token_file = open('./data/tokens.csv', 'r')

                for token_entry in token_file:
                    token_data_string = token_entry.strip().split(',')
                    if token in token_entry:
                        print(token_data_string)
                        print(token_data_string[0])
                        print(user_name)
                        if token_data_string[0] != user_name:
                            self.send_response(401)
                            self.end_headers()
                        else:
                            self.send_response(200)
                            self.end_headers()
                            delete_item_from_json(data_type, int(json_id), token)

            elif path_list[1] == 'albums':
                user_name = ''
                token_file = open('./data/tokens.csv', 'r')

                for token_entry in token_file:
                    token_data_string = token_entry.strip().split(',')
                    if token in token_entry:
                        print(token_data_string)
                        print(token_data_string[0])
                        print(user_name)
                        if token_data_string[0] != user_name:
                            self.send_response(401)
                            self.end_headers()
                        else:
                            self.send_response(200)
                            self.end_headers()
                            delete_item_from_json(data_type, int(json_id), token)

            elif path_list[1] == 'playlists':
                pass

    def do_PUT(self):
        pass

    def do_POST(self):
        path_list = self.path.split('/')
        print(path_list)

        if len(path_list) == 2:  # create a new user
            if 'users' in path_list[1]:
                user_id = create_user(path_list)
                if user_id != -1:
                    self.send_response(301)
                    self.send_header('New User', 'http://localhost:8000/users/' + str(user_id))
                    self.end_headers()
                else:
                    self.send_response(405)
                    self.end_headers()

            # search spotify albums
            elif path_list[1] == 'albums':
                token = get_spotify_token()
                print(path_list)
                album_data = search_spotify(token, ['album', 'ye'])
                album_data = json.dumps(album_data)

                # form_page = """<!DOCTYPE html>
                #                 <html>
                #                 <body>
                #
                #                 <h2>Album Search Results</h2>
                #                 <h3>Check albums and then click submit to save</h3>
                #
                #                 <form action="http://localhost:8000/playlists" method="post">
                #                   """
                #
                # for key, value in album_data.items():
                #     print(key)
                #
                # form_page += """<input type="checkbox" name="sample" value="artist" /> Artist_name <br>
                #                 <input type="checkbox" name="sample" value="artist2" /> Another_artist <br>"""
                #
                # form_page += """<input type="submit" value="Submit">
                #                 </form>
                #
                #                 </body>
                #                 </html>"""

                self.send_response(200)
                self.end_headers()
                self.wfile.write(album_data.encode())


            # search spotify playlists
            elif path_list[1] == 'playlists':

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"great success")
                self.wfile.write(str(self.responses).encode())
                # content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
                # post_data = self.rfile.read(content_length)
                # print(post_data)
                # print(self.headers)
                # spotify_token = get_spotify_token()
                # query = path_list
                # search_spotify(spotify_token, query)

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


def delete_item_from_json(operation, item_id, token):
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


def add_user_playlist(userdata, userid, playlistid, token):
    if validate_token(token):
        for user in userdata:
            if user['id'] == userid:
                user['playlists'].append(playlistid)
                return userdata

    return None


def get_user_pass(path_list):
    index = len(path_list) - 1
    user_name_index = path_list[index].find('user_name=') + len('user_name=')
    and_index = path_list[index].find('&', user_name_index)
    password_index = path_list[index].find('password=', and_index) + len('password=')

    user_name = path_list[index][user_name_index:and_index]
    password = path_list[index][password_index:]

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


def get_spotify_token():
    client_id = '5012223408634ccb90deea3f0cf85718'
    client_secret = 'bc1d37409b8046c6986c054ec3d4b4f6'

    url = 'https://accounts.spotify.com/api/token'
    payload = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'}
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    token = requests.post(url, data=payload, headers=headers)
    json_resp = json.loads(token.content)
    return json_resp['access_token']


def search_spotify(token, query):
    # query is a list of terms to search for
    # query[0] is what type of item they are going to search for
    # query[1] is the physical search term, e.g. artist name or album name
    url = 'https://api.spotify.com/v1/search'

    # query = [type, name to filter type]
    # spotify api reference: https://developer.spotify.com/documentation/web-api/reference/search/search/
    payload = {'q': query[1], 'type': query[0]}
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get('https://api.spotify.com/v1/search', params=payload, headers=headers)
    response_json = json.loads(response.content)

    return response_json


def generate_page_from_json(type, data):
    page = """ <!DOCTYPE html>
                    <html>
                    <head>
                        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                    </head>
                    <body>
                    <div class="container">
                    """

    if type == 'albums':
        page += '<h1>Album Data</h1><br>'
        for album in data:
            page += '<h3>' + album['album_title'] + '</h3>'
            page += '<p>' + album['artist_name'] + '</p>'
            page += '<p>' + album['label_name'] + '</p>'
            page += '<p>' + album['release_date'] + '</p>'
    if type == 'album':
        page += '<h1>Album Data</h1><br>'
        page += '<h3>' + data['album_title'] + '</h3>'
        page += '<p>' + data['artist_name'] + '</p>'
        page += '<p>' + data['label_name'] + '</p>'
        page += '<p>' + data['release_date'] + '</p>'
    elif type == 'playlists':
        page += '<h1>Playlist Data</h1><br>'
        for playlist in data:
            page += '<h3>' + playlist['playlist_title'] + '</h3>'
            page += '<p>' + str(playlist['track_list']) + '</p>'

    elif type == 'playlist':
        page += '<h1>Playlist Data</h1><br>'
        page += '<h3>' + data['playlist_title'] + '</h3>'
        page += '<p>' + str(data['track_list']) + '</p>'
    elif type == 'artists':
        pass

    page += '</div></body></html>'
    return page


def generate_spotify_page(query_type, data):
    page = """ <!DOCTYPE html>
                <html>
                <head>
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                </head>
                <body>
                <div class="container">
                """

    if query_type == 'artist':
        page += "<h2>Artist Search Results</h2>"

        data = data['artists']['items']

        for item in data:
            page += '<div>'
            page += str(item['name'])
            page += '<br>'
            if len(item['images']) > 0:
                page += '<img src="' + item['images'][2]['url'] + '" alt="Italian Trulli">'
            page += '</div>'

    elif query_type == 'album':
        page += "<h1>Album Search Results</h1>"
        page += '<h3>Check albums to save them. Then click the submit button.</h3>'
        page += '<input type="submit" value="Submit">'

        # form start
        page += '<form action="http://localhost:8000/query" method="post">'

        data = data['albums']['items']

        for item in data:
            print(item)
            page += '<input type="checkbox" value="' + item['id'] + '">'
            page += '<div>'

            # add album Name
            page += '<h3>' + str(item['name']) + '</h3>'

            # print out artist names on album
            for artist in item['artists']:
                page += '<p>' + str(artist['name']) + '</p>'
                print(artist['name'])

            page += '<br>'
            if len(item['images']) > 0:
                page += '<img src="' + item['images'][1]['url'] + '" alt="Italian Trulli">'

            page += '</div>'
            page += '<br>'
            page += '<br>'

    elif query_type == 'playlist':
        page += "<h1>Playlist Search Results</h1>"
        page += '<h3>Check playlists to save them. Then click the submit button.</h3>'
        page += '<input type="submit" value="Submit">'

        # form start
        page += '<form action="http://localhost:8000/query" method="post">'

        data = data['playlists']['items']

        for item in data:

            page += '<input type="checkbox" value="' + item['id'] + '">'

            # add playlist Name
            page += '<h3>' + str(item['name']) + '</h3>'

            # add images
            page += '<br>'
            if len(item['images']) > 0:
                page += '<div id="' + str(item['id']) + '">'
                page += '<img src="' + item['images'][0]['url'] + '" alt="Italian Trulli">'
                page += '<br>'
                page += '</div>'

    page += '<br>'

    page += '</form></div></body></html>'
    return page


def clean_tokens():
    fp = open('./data/tokens.csv', 'r', encoding='UTF-8')
    new_data = ''
    new_data += fp.readline()

    for line in fp:
        data = line.strip().split(',')
        if data[2] < str(datetime.now()):
            pass
        else:
            new_data += line

    fp.close()
    fp = open('./data/tokens.csv', 'w', encoding='UTF-8')
    fp.write(new_data)
    fp.close()


def main():
    listen_port = 8000
    httpd = HTTPServer(('localhost', listen_port), SimpleHTTPRequestHandler)
    print('cleaning local data..')
    clean_tokens()
    print('now listening on port:' + str(listen_port))
    httpd.serve_forever()


if __name__ == '__main__':
    main()
