import requests


def main():
    url = 'http://localhost:8000/'

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
    #token = requests.post('localhost:8000/users/{id}/token ?user_name=admin&password=admin')
    #assert token.status_code == 200


if __name__ == '__main__':
    main()
