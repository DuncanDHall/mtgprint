# Generates a set of cards based on user input
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

# prompt for number of rares/mythics, uncommons, and commons, or number of packs
packs_or_cards = input("Would you like to generate packs or a custom distribution of rarities? (p/c) ")

while not packs_or_cards in ["p", "", "c"]:
    packs_or_cards = input("Would you like to generate packs or a custom distribution of rarities? Input 'p' for packs or 'c' for custom distribution: ")

if packs_or_cards in ["p", ""]:
    mythic_probability = 0.125
    num_packs = int(input("How many packs would you like to generate? "))
    num_mythics = sum([1 if random.random() < mythic_probability else 0])
    num_rares = 1 * num_packs - num_mythics
    num_uncommons = 3 * num_packs
    num_commons = 10 * num_packs
elif packs_or_cards in ["c"]:
    num_mythics = input("How many mythics would you like to generate? ")
    num_rares = input("How many rares would you like to generate? ")
    num_uncommons = input("How many uncommons would you like to generate? ")
    num_commons = input("How many commons would you like to generate? ")

save_key = input("Please input a unique save key: ")


# Load csv card collection
print("Loading cards...")
collection = []
with open(card_list_file) as csv_file:
    for row in csv.reader(csv_file):
        collection.append(row)

# Separate by rarity
mythics = []
rares = []
uncommons = []
commons = []

for name, label, img_url in collection:
    if "mythic" in label:
        mythics.append((name, img_url))
    if "rare" in label:
        rares.append((name, img_url))
    elif "uncommon" in label:
        uncommons.append((name, img_url))
    elif "common" in label:
        commons.append((name, img_url))

# Create new directory for sheets to be saved
dir = "cards/" + str(datetime.today().strftime("%m-%d-%y-{}/".format(save_key)))
print("Sheets will be saved at {}".format(dir))
os.makedirs(dir)

cards = []

# Randomize cards
print("Picking cards...")
for m in range(num_mythics):
    cards.append(random.choice(rares))
for r in range(num_rares):
    cards.append(random.choice(rares))
for u in range(num_uncommons):
    cards.append(random.choice(uncommons))
for c in range(num_commons):
    cards.append(random.choice(commons))

# Fetch card images
print("Fetching card images...")
imgs = []
num_cards = len(cards)
for i, card in enumerate(cards):
    name, img_url = card

    print(" {}/{}\t{}".format(i, num_cards, name))
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
    path = dir + "sheet{}.jpg".format(i)
    sheet.save(path)

print("done")
