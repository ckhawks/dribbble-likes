import urllib
import requests
from lxml import html

likesPage = "driblike.htm"

username = "lucnoe"

likesUrl = "https://dribbble.com/" + username + "/likes"

#page = urllib.urlopen(likesUrl).read()
page = requests.get(likesUrl)
tree = html.fromstring(page.content)

likesText = tree.xpath('//*[@id="main"]/h2/text()')

# this doesnt work because we are not authorized
# the plan was to download the first page and then get # of likes from header
# then keep going to each next page until page * 24 > # likes
# https://dribbble.com/Stellaric/likes?page=2&per_page=24

likesText = likesText.replace(" Likes", "")
total = int(likesText)

print("they have " + str(total) + " likes")

'''

# get your likes page by going to your profile's likes, scrolling all the way down, and then right click and hit save as and then place it in the same directory as this script

page = urllib.urlopen(likesPage).read()
tree = html.fromstring(page) #.content

likes = tree.xpath('//a[@class="dribbble-over"]/@href')

print("Likes: ", likes)

with open('likes.txt', 'w') as f:
    for item in likes:
        print >> f, item

'''
