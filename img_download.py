import requests
import json

img_links = list()
img_names = list()
with open("schools.json", encoding="utf-8") as r:
    data = json.load(r)

    for item in data['institutes']:

        if item['logo'] != '':
            img_links.append(item['logo'])
            img_names.append(item['name'])

        # print("{} \t {} ".format(item['logo'], item['name']))

for i, link in enumerate(img_links):
    response = requests.get(link)

    with open("{}.jpg".format(img_names[i]), "wb") as f:
        f.write(response.content)
