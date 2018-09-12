# json to csv for reddit
# items to store in csv: date of query, date of post (readable), title of post, number of upvotes, its url

import requests
import json
import csv
import datetime

#get data
data = requests.get('http://www.reddit.com/.json', headers = {'User-agent':'testing'}).json()

post_data = data['data']['children']

#write data to file

with open('reddit_data.csv', mode='a') as reddit_file:
    reddit_writer = csv.writer(reddit_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for item in post_data:

        post_attributes = item['data']
        
        query_date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print(datetime.datetime.today())
        post_date = post_attributes['created']
        post_date = datetime.datetime.utcfromtimestamp(post_date).strftime('%Y-%m-%d %H:%M:%S')
        post_title = post_attributes['title']
        post_upvotes = post_attributes['ups']
        post_url = post_attributes['url']

        reddit_writer.writerow([query_date, post_date, post_title, post_upvotes, post_url])