# Generates a set of cards for a booster and assembles them in pdf form
# created June 24, 2017

import urllib.request
from PIL import Image
import io
import csv
import random


# Load csv card collection
print("Loading cards...")
collection = []
with open("beta_cards.csv") as csv_file:
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

# Randomize booster
print("Drawing cards for booster...")
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
    sheet.save("sheet" + str(i) + ".jpg")


print("done")
