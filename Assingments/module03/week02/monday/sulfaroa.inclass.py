# use the imgur API and get the most popular cat picture
"""
sulfaroa
9/10/18
In-class activity
"""

from imgurpython import ImgurClient
import requests

client_id = '82d55c3dec952aa'
client_secret = '3e2e0865723e9a6b94100702980b58ca95a0fd25'

client = ImgurClient(client_id, client_secret)

# get images with cat
tag_collection = client.gallery_search('cat', advanced=None, sort='top', page=0)

# slice out first image
image_url = tag_collection[0].link

# get image then write it
img_data = requests.get(image_url).content
with open('cat_picture.jpg', 'wb') as handler:
    handler.write(image_url)