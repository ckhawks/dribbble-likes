import urllib
import urllib.request
import requests
import re
from lxml import html

link = 'https://dribbble.com/shots/4449294-Travel-Map-Personal'
dl = 0
verbose = True

directory = "images/"

with open('likes.txt') as f:
    lines = f.read().splitlines()

print("Downloading " + str(len(lines)) + " shots to " + directory)


i = 0
for shot in lines:

    link = shot

    # get title to use as filename
    title = link.replace("https://dribbble.com/shots/", "")

    # gets main page
    page = requests.get(link)
    tree = html.fromstring(page.content)

    # get title to use in verbose
    titleVerbose = tree.xpath('//*[@id="content"]/div[2]/header/div/h1/text()');
    authorVerbose = tree.xpath('//*[@id="content"]/div[2]/header/div/h2/span[1]/span/a/text()')
    print("Downloading '" + titleVerbose[0] +"\' by \'" + authorVerbose[0] + "'")

    # gets main image png link
    info = tree.xpath('//*[@id="content"]/div[2]/div[1]/div[1]/@data-img-src')
    if verbose:
        print(" - " + info[0])
    ext = re.findall(".[0-9a-z]+$", info[0])
    urllib.request.urlretrieve(info[0], directory + title + "" + str(dl) + ext[0])

    # gets attachments
    attachmentsul = tree.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div/ul/*')
    #print(attachmentsul)

    # download each attachment picture
    for li in attachmentsul:
        dl = dl + 1
        thing = li.xpath('a/img/@src')
        if len(thing) > 0:
            # get source image
            thing[0] = thing[0].replace('thumbnail/', '')
            if verbose:
                print(" - " + thing[0])

            #get file extension
            ext = re.findall(".[0-9a-z]+$", thing[0])
            urllib.request.urlretrieve(thing[0], directory + title + "" + str(dl) + ext[0])
        else: # probably an mp4
            mp4Link = li.xpath('a/@href')
            mp4File = li.xpath('a/text()')
            url = "https://dribbble.com" + mp4Link[0] + "/" #+ mp4File[0]
            #https://cdn.dribbble.com/users/1047455/screenshots/5261914/attachments/1141504/ig_6.mp4

            if verbose:
                print(" - " + url)

            #get file extension
            ext = re.findall(".[0-9a-z]+$", mp4File[0])
            r = requests.get(url, allow_redirects=True)
            open(directory + title + "" + str(dl) + ext[0], 'wb').write(r.content)

    i = i + 1

'''

import urllib

from lxml import html
page = urllib.urlopen("driblike.htm").read()
print page

tree = html.fromstring(page) #.content


' ''
//*[@id="screenshot-4326410"]/div/div[1]/div/a[2]
//*[@id="screenshot-4362169"]/div/div[1]/div/a[2]
#screenshot-4362169 > div > div.dribbble-shot > div > a.dribbble-over
//*[@id="screenshot-4362169"]/div/div[1]/div/a[2]

//a/@href
//div[@class="dribbble-over"]//a/@href

'' '

#This will create a list of buyers:
buyers = tree.xpath('//a[@class="dribbble-over"]/@href')

print "Buyers: ", buyers

with open('likes.txt', 'w') as f:
    for item in buyers:
        print >> f, item
'''
