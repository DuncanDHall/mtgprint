# Generates a set of cards for a booster and assembles them in pdf form
# created June 24, 2017
import os
import urllib.request
from datetime import datetime

from PIL import Image
import io
import csv
import random
import sys


# the source for the image urls
card_list_file = "amonkhet_cards.csv"

# rarity distribution
mythic_probability = 0.1
num_rares = 1
num_uncommons = 3
num_commons = 10

# Unpack args or prompt for them
if len(sys.argv) == 3:
    num_packs = sys.argv[1]
    save_key = sys.argv[2]
else:
    num_packs = int(input("How many packs would you like to generate? "))
    save_key = input("Please input a unique save key: ")


# Load csv card collection
print("Loading cards...")
collection = []
with open(card_list_file) as csv_file:
    for row in csv.reader(csv_file):
        collection.append(row)

# Separate by rarity
rares = []
uncommons = []
commons = []

for name, label, img_url in collection:
    if "rare" in label:
        rares.append((name, img_url))
    elif "uncommon" in label:
        uncommons.append((name, img_url))
    elif "common" in label:
        commons.append((name, img_url))

# Create new directory for sheets to be saved
dir = "boosters/" + str(datetime.today().strftime("%m-%d-%y-{}/".format(save_key)))
print("Sheets will be saved at {}".format(dir))
os.makedirs(dir)

# for multiple boosters
for b in range(num_packs):

    # Randomize booster
    print("Drawing cards for booster #{}...".format(b))
    booster = []
    for i in range(1):  # one rare
        booster.append(random.choice(rares))
    for i in range(3):  # three uncommons
        booster.append(random.choice(uncommons))
    for i in range(11):  # eleven commons
        booster.append(random.choice(commons))

    # Fetch card images
    print("Fetching card images...")
    imgs = []
    for name, img_url in booster:
        print("\t- " + name)
        file_data = urllib.request.urlopen(img_url)
        imgs.append(Image.open(io.BytesIO(file_data.read())))

    # anti-alias all images artificially increasing quality to 200%
    print("Resizing card images...")
    for i in range(len(imgs)):
        new_size = imgs[i].size[0] * 2, imgs[i].size[1] * 2
        imgs[i] = imgs[i].resize(new_size, Image.ANTIALIAS)

    # arrange onto 3x3 grid
    print("Laying out print sheets...")
    cols = 3
    rows = 3
    card_width, card_height = imgs[0].size
    sheets = []
    i = 0
    cards_left = True
    while cards_left:
        sheet = Image.new('RGB', (card_width * 3, card_height * 3), (255, 255, 255))
        x = y = 0
        for row in range(rows):
            for col in range(cols):
                if i < len(imgs):
                    sheet.paste(imgs[i], (x, y))
                    x += card_width
                    i += 1
                else:
                    cards_left = False
            x = 0
            y += card_height
        sheets.append(sheet)

    # Save the result
    print("Saving layouts...")

    for i, sheet in enumerate(sheets):
        path = dir + "b{}s{}.jpg".format(b, i)
        sheet.save(path)

    print("Booster #{} complete\n".format(b))


print("done")
