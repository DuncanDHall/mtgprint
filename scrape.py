# This is a short script which harvests image links from magiccards.info
# created June 23, 2017

# for images:
# http://magiccards.info/query?q=e%3Abe%2Fen&v=card&s=cname&p=1
# http://magiccards.info/query?q=e%3Abe%2Fen&s=cname&v=card&p=15

# only rares:
# http://magiccards.info/query?q=r%3Arare+e%3Abe%2Fen&v=card&s=cname
import csv
import re
import urllib.request

# html sources
beta_rares_url = "http://magiccards.info/query?q=r%3Arare+e%3Abe%2Fen&v=card&s=cname"
beta_uncommons_url = "http://magiccards.info/query?q=r%3Auncommon+e%3Abe%2Fen&v=card&s=cname"
beta_commons_url = "http://magiccards.info/query?q=r%3Acommon+e%3Abe%2Fen&v=card&s=cname"
first_page_urls = [beta_rares_url, beta_uncommons_url, beta_commons_url]
query_rarity = ["beta rare", "beta uncommon", "beta common"]
queries = zip(query_rarity, first_page_urls)

# re patterns
card_image_url_pattern = re.compile('<img src="(http://magiccards.info/scans/en/be/\d+.jpg)"')
card_title_pattern = re.compile('<a href="/be/en/\d+\.html">(.*)</a>')

# iterate through queries extracting card names and image links
collection = []

for label, url in queries:
    # grab html for all pages associated with that query
    previous_first_card = ""
    page_num = 1

    # import pudb; pu.db

    while True:
        # collect all image links and card titles on this page
        full_url = url + "&p=" + str(page_num)
        html = urllib.request.urlopen(full_url).read().decode('utf-8')
        card_titles = re.findall(card_title_pattern, html)
        card_image_links = re.findall(card_image_url_pattern, html)

        # just in case
        if len(card_titles) != len(card_image_links):
            raise Exception(
                "page scraped incorrectly: found titles do not match found image urls for " + url + "&p=" + page_num
            )

        # this site serves the highest available page if we've run out
        if previous_first_card == card_titles[0]:
            break
        else:
            entries = [(card_titles[i], label, card_image_links[i]) for i in range(len(card_titles))]
            collection.extend(entries)
            previous_first_card = card_titles[0]
            print("completed " + label + " page " + str(page_num))
            page_num += 1


# store that collection
writer = csv.writer(open("beta_cards.csv", "w"))
head = ("Title", "Rarity", "Image URL")
writer.writerow(head)
for entry in collection:
    writer.writerow(entry)

print("scrape complete and saved at ./beta_cards.csv\n")
