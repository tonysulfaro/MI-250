import requests
import json


def get_users():
    url = 'http://localhost:8000/'
    users = requests.get(url + 'users').json()

    for user in users:
        print(user)


def main():
    url = 'http://localhost:8000/'

    print('querying server at: ' + url)

    # get on bulk of data
    users = requests.get(url + 'users')
    assert users.status_code == 200

    albums = requests.get(url + 'albums')
    assert albums.status_code == 200

    playlists = requests.get(url + 'playlists')
    assert playlists.status_code == 200

    # check invalid paths
    no_item = requests.get(url + 'no_item')
    assert no_item.status_code == 404

    # user that doesn't exist
    no_user = requests.get(url + 'users/999')
    assert no_user.status_code == 404

    # check if token request working
    # token = requests.post('localhost:8000/users/{id}/token ?user_name=admin&password=admin')
    # assert token.status_code == 200

    print('Server functional, tests passed.')
    print()

    client_id = '5012223408634ccb90deea3f0cf85718'
    client_secret = 'bc1d37409b8046c6986c054ec3d4b4f6'

    url = 'https://accounts.spotify.com/api/token'
    payload = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'}
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    # response = requests.post(url, data=payload, headers=headers)
    # json_resp = json.loads(response.content)
    # print(json_resp['access_token'])

    token = 'BQDkDzdvEhWOO2aqllHvL1LuZf5iX3455Bo0NSYr36V1D1a2fpIjNZSvumqaDfDCPAElOcrOjXfVUUaXyEE'



#     instructions = """
#  Enter a command:
#  L: Login to the service
#  A: Display ll albums stored
#  P: Display all playlists stored
#  U: Display all users
#
#  Q: Exit the program
# """
#
#     user_input = ''
#     while user_input != 'q':
#         user_input = input(instructions).lower()
#
#         if user_input == 'u':
#             get_users()


if __name__ == '__main__':
    main()
