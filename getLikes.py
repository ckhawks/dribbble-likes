import urllib
import urllib.request
import re
import requests
from lxml import html

username = "fill"

likesUrl = "https://dribbble.com/" + username + "/likes"

user = "fill"
password = "fill"

with requests.Session() as login_session:
    login_session.headers.update({"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})
    landing = login_session.get("https://dribbble.com/session/new")
    #landing_soup = BeautifulSoup(landing.text, "html.parser")
    #authenticity_token = landing_soup.find(attrs={"name":"authenticity_token"})["value"]
    tree = html.fromstring(landing.content)
    nonce = tree.xpath('//*[@id="form-oldschool"]/form/input[2]/@value')[0]
    authenticity_token = nonce
    print(authenticity_token)
    login_request = login_session.post("https://dribbble.com/session", data={"utf8": "✓", "authenticity_token": authenticity_token, "login": user, "password": password})
    # print(login_session.cookies)
    likes_page = login_session.get(likesUrl)
    #print(likes_page.text)
    tree = html.fromstring(likes_page.content)
    likesText = tree.xpath('//*[@id="main"]/h2/text()')[0]

    likesText = likesText.replace(" Likes", "")
    total = int(likesText)

    print("they have " + str(total) + " likes")

    required_pages = total / 24 + 1

    likes = tree.xpath('//a[@class="dribbble-over"]/@href')

    page = 2
    while page < required_pages:
        likes_next_page = login_session.get(likesUrl + "?page=" + str(page) + "&per_page=24")
        tree = html.fromstring(likes_next_page.content)
        likes = likes + tree.xpath('//a[@class="dribbble-over"]/@href')
        page = page + 1
    print(likes)
    print(str(len(likes)))

    #link = 'https://dribbble.com/shots/4449294-Travel-Map-Personal'
    dl = 0
    verbose = True

    directory = "images/"

    lines = likes

    print("Downloading " + str(len(lines)) + " shots to " + directory)


    i = 0
    for shot in lines:

        link = "https://dribbble.com" + shot

        # get title to use as filename
        title = link.replace("https://dribbble.com/shots/", "")

        # gets main page
        print(str(i) + ": " + link)
        page = requests.get(link)
        tree = html.fromstring(page.content)

        # get title to use in verbose
        titleVerbose = tree.xpath('//*[@id="content"]/div[2]/header/div/h1/text()');
        authorVerbose = ""
        authorVerbose = tree.xpath('//*[@id="content"]/div[2]/header/div/h2/span[1]/span/a/text()')

        if(len(authorVerbose) == 0):
            authorVerbose = tree.xpath('//*[@id="content"]/div[2]/header/div/h2/span[1]/span/text()')
            authorVerbose[0] = authorVerbose[0].strip().replace("by ", "")
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
