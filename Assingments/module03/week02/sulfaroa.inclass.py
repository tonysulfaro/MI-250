# use the imgur API and get the most popular cat picture

from imgurpython import ImgurClient

client_id = '82d55c3dec952aa'
client_secret = '3e2e0865723e9a6b94100702980b58ca95a0fd25'

client = ImgurClient(client_id, client_secret)

# Example request
#items = client.gallery(section='top', sort='time', page=0, window='week', show_viral=True)
#for item in items:
    #print(item.link)

tag_collection = client.gallery_search('cat', advanced=None, sort='top', page=0)

print(tag_collection[1].link)