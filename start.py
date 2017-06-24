# for images:
# http://magiccards.info/query?q=e%3Abe%2Fen&v=card&s=cname&p=1
# http://magiccards.info/query?q=e%3Abe%2Fen&s=cname&v=card&p=15

# only rares:
# http://magiccards.info/query?q=r%3Arare+e%3Abe%2Fen&v=card&s=cname
import csv
import re
import urllib.request

# html source
target_url = "http://magiccards.info/query?q=r%3Arare+e%3Abe%2Fen&v=card&s=cname&p=1"

# re patterns
card_image_url_pattern = re.compile('<img src="http://magiccards.info/scans/en/be/\d+.jpg"')
card_title_pattern = re.compile('<a href="/be/en/\d+\.html">(.*)</a>')

# source html
html = urllib.request.urlopen(target_url).read().decode('utf-8')

# collect all image links and card titles on this page
card_image_links = re.findall(card_image_url_pattern, html)
card_titles = re.findall(card_title_pattern, html)
collection = zip(card_titles, card_image_links)

# store that collection
writer = csv.writer(open("beta_cards.csv", "w"))
head = ("Title", "Image URL")
writer.writerow(head)
for entry in collection:
    writer.writerow(entry)
    print(entry)
