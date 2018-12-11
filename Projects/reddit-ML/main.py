import requests
import json
import os.path
import pandas as pd
import numpy as np
from flask import Flask
from flask import request
from flask import jsonify


def collect_data(filename, subreddit):
    '''
    saves new subreddit posts in json file
    :param filename: file to store data (in json)
    :param subreddit: subreddit to get data from
    :return:
    '''
    url = 'https://api.pushshift.io/reddit/submission/search/?&subreddit=' + subreddit + '&size=1000'
    response = requests.get(url)
    json_resp = response.text

    if os.path.isfile(filename):
        with open(filename, 'r', encoding='UTF-8') as file:
            before = json.loads(file.read())
            json_resp = json.loads(json_resp)

            print(before['data'])
            print(json_resp['data'])

            before['data'] += json_resp['data']
        with open(filename, 'w', encoding='UTF-8') as file:
            file.write(json.dumps(before))
            return json.dumps(before)

    else:
        with open(filename, 'w') as file:
            file.writelines(json)
            file.close()
            return json


def get_user_data(user_id):
    pass


def collect_updated_post_data(basefile, updated_save):
    """
    get and save updated post data to csv
    :param basefile:
    :param updated_save:
    :return: None
    """

    comments_for_post_id = 'https://api.pushshift.io/reddit/submission/comment_ids/<post_id>'
    post_by_id = 'https://api.pushshift.io/reddit/submission/search?ids='

    user_fp = open(basefile, 'r', encoding='UTF-8')
    json_data = json.loads(user_fp.read())

    newest_data = {'data': []}

    for post in json_data['data']:
        # print(post['id'])
        # print(post['score'])
        updated_post = requests.get(post_by_id + post['id']).json()['data'][0]
        newest_data['data'].append(updated_post)
        print('updated post', post['id'])

    updated_json = json.dumps(newest_data)

    with open(updated_save, 'w', encoding='UTF-8') as file:
        file.write(updated_json)


def load_json_to_dict(filename):
    diff_data = {}

    before = {}

    with open(filename, 'r', encoding='UTF-8') as file:
        before = json.loads(file.read())

    for post in before['data']:
        diff_data[post['id']] = post['score']

    for key, value in diff_data.items():
        print(key, value)

    print(len(diff_data.keys()))


def clean_data(filename):
    user_fp = open(filename, 'r', encoding='UTF-8')
    json_data = json.loads(user_fp.read())

    print(json_data)
    print(len(json_data['data']))
    with open(filename, 'w', encoding='UTF-8') as file:
        file.write(json.dumps(json_data))


def train_model(filename, outfile):
    # load flat file into data structure
    user_fp = open(filename, 'r', encoding='UTF-8')
    json_data = json.loads(user_fp.read())

    out_fp = open(outfile, 'w', encoding='UTF-8')

    """
    Fields to extract from JSON
    
    author
    author_patreon_flair
    can_mod_post
    contest_mode
    created_utc - convert to 24h time
    gildings
        gid_1
        gid_2
        gid_3
    id
    is_crosspostable
    is_meta
    is_original_content
    is_robot_indexable
    is_self
    locked
    num_comments
    num_crossposts
    over_18
    retrieved_on
    score
    hidden
    spoiler
    pinned
    stickied
    title
    whitelist_status
    """

    for post in json_data['data']:
        print(post['author'])

        author = post['author']
        author_patreon_flair = post['author_patreon_flair']
        can_mod_post = post['can_mod_post']

        tup = tuple()
    print(len(json_data['data']))


def predict_score(post):
    pass


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/refresh-data/', methods=['POST'])
def show_user_profile():
    file = request.args.get('file')
    subreddit = request.args.get('subreddit')
    # show the user profile for that user
    data = collect_data(file, subreddit)
    return (data)


def main():
    app.run(host='0.0.0.0', port=9999)

    # file = 'askreddit-initial.json'
    # outfile = 'askreddit-initial.csv'
    # collect_data('askreddit-initial.json', 'askreddit')
    # collect_updated_post_data('writingprompts-initial.json', 'writingprompts-final.json')
    # time.sleep()
    # load_json_to_dict('writingprompts-initial.json')
    # clean_data('showerthoughts-initial.json')
    # train_model(file, outfile)


if __name__ == '__main__':
    main()
