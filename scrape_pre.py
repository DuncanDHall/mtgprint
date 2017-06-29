# This is a short script which harvests image links from magiccards.info
# created June 23, 2017

import csv
import re
import urllib.request

# html sources

# for hour of devastation
file_name = "hour_of_devestation_cards.csv"
cards_url = "http://mythicspoiler.com/hou/index.html"
image_url_template = "http://mythicspoiler.com/hou/cards/{}.jpg"

# re patterns
card_stem_url = re.compile('<a class="card" href="cards/[a-zA-Z0-9]+.html"><img width="200" align="left" hspace="0" src="cards/([a-zA-Z0-9]+).jpg"></a>')

collection = []

# collect all image links and card titles on this page
html = urllib.request.urlopen(cards_url).read().decode('utf-8')
card_titles = re.findall(card_stem_url, html)
card_image_links = [image_url_template.format(title) for title in card_titles]

# this site serves the highest available page if we've run out
entries = [(card_titles[i], "", card_image_links[i]) for i in range(len(card_titles))]
collection.extend(entries)

# store that collection
writer = csv.writer(open(file_name, "w"))
head = ("Title", "Rarity", "Image URL")
writer.writerow(head)
for entry in collection:
    writer.writerow(entry)

print("scrape complete and saved at ./" + file_name + "\nNote that rarities are NOT INCLUDED")
