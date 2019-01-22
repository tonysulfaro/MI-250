import requests
import json
import os.path
import pandas as pd
import numpy as np
from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from sklearn import linear_model


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


def load_from_csv(filename):
    data = pd.read_csv(filename, error_bad_lines=False)
    print(data)
    return data


def load_to_csv(filename, outfile):
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
        # author_patreon_flair = post['author_patreon_flair']
        can_mod_post = post['can_mod_post']
        contest_mode = post['contest_mode']

        created_utc = post['created_utc']

        gildings1 = post['gildings']['gid_1']
        gildings2 = post['gildings']['gid_2']
        gildings3 = post['gildings']['gid_3']

        post_id = post['id']
        is_crosspostable = post['is_crosspostable']
        is_meta = post['is_meta']
        is_original_content = post['is_original_content']
        is_robot_indexable = post['is_robot_indexable']
        is_self = post['is_self']
        locked = post['locked']
        num_comments = post['num_comments']
        num_crossposts = post['num_crossposts']
        over_18 = post['over_18']
        score = post['score']
        # hidden = post['hidden']
        spoiler = post['spoiler']
        pinned = post['pinned']
        stickied = post['stickied']
        title = post['title']
        whitelist_status = post['whitelist_status']

        tup = author, can_mod_post, contest_mode, created_utc, gildings1, gildings2, gildings3, post_id, is_crosspostable, is_meta, is_original_content, is_robot_indexable, is_self, locked, num_comments, num_crossposts, over_18, score, spoiler, pinned, stickied, title, whitelist_status
        out_fp.writelines(str(tup)[1:-1] + '\n')

    print(len(json_data['data']))


def predict_score(post, filename):
    # pandas dataframe
    df = load_from_csv(filename)

    # use ElasticNet Lasso to predict score because it is predicting a quantity, has < 100k samples
    # should probably take all the entries from the csv as dimensions and reduce them to make predictions
    print(df.head())


def post_stats(filename):
    max_comments = 0
    max_post = ''

    min_comments = float('inf')
    min_post = ''

    with open(filename, 'r', encoding='UTF-8') as file:
        for line in file:
            line = line.split(',')

            num_comments = int(line[14])
            score = int(line[17])
            print(score, num_comments)

            if num_comments > max_comments:
                max_comments = score
                max_post = line

            if num_comments < min_comments:
                min_comments = score
                min_post = line

        print(max_comments, max_post)
        print(min_comments, min_post)


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
    # app.run(host='0.0.0.0', port=9999)

    file = 'askreddit-initial.json'
    outfile = 'askreddit-initial.csv'
    # collect_data('askreddit-initial.json', 'askreddit')
    # collect_updated_post_data('askreddit-initial.json', 'askreddit-final.json')
    # time.sleep()
    # load_json_to_dict('writingprompts-initial.json')
    # clean_data('showerthoughts-initial.json')
    # load_to_csv(file, outfile)
    #load_from_csv(outfile)
    predict_score('3kjlj3j4', outfile)
    #post_stats(outfile)


if __name__ == '__main__':
    main()
