import requests
import json


def collect_data(filename, subreddit):
    '''
    saves new subreddit posts in json file
    :param filename: file to store data (in json)
    :param subreddit: subreddit to get data from
    :return:
    '''
    url = 'https://api.pushshift.io/reddit/submission/search/?&subreddit=' + subreddit + '&size=1000'
    response = requests.get(url)
    json = response.text

    with open(filename, 'w') as file:
        file.writelines(json)
        file.close()


def get_user_data(user_id):
    pass


def save_updated_post_data(basefile, updated_save):
    """
    get and save updated post data to csv
    :param basefile:
    :param updated_save:
    :return: None
    """

    comments_for_post_id = 'https://api.pushshift.io/reddit/submission/comment_ids/<post_id>'
    json_data = ''

    with open(basefile, 'r') as file:
        json_data = file.read()
        file.close()

    json_data = json.loads(json_data)

    with open(updated_save, 'w') as file:
        file.writelines()


def parse_json(filename):
    pass


def train_model(filename):
    # load flat file into data structure
    pass


def predict_score(post):
    pass


def main():
    collect_data('askreddit.json', 'askreddit')


if __name__ == '__main__':
    main()
