import requests
from bs4 import BeautifulSoup
import json


url = 'http://www.ecolia.ma/ecole-etablissement-el-bilia-931'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


def contact_scraper(selector):
    contact = bloc_info.find(class_=selector)
    contact_list = []
    contact_list.append(contact.get_text())

    # other contact infos
    if contact.find_parent().find("ul", {"class": "dropdown"}):

        for item in contact.find_parent().select("ul", {"class": "dropdown"}):
            for other_nums in item.select("li"):
                if other_nums.get_text() != ' ':
                    contact_list.append(other_nums.get_text())

    return contact_list


def get_link(a):
    if a.text != 'Cliquer pour remplir':
        return a["href"]
    else:
        return ''


info = {}

# get the name
info['name'] = soup.find(class_="denomination").get_text()


# Levels
levels = ''
all_levels = soup.select(".entite-existe")
for label in all_levels:
    if levels != '':
        info['levels'] = "{}, {}".format(levels, label.find("span").get_text())
    else:
        info['levels'] = label.find("span").get_text()


# bloc with the main information
bloc_info = soup.find(class_="ecole-bloc-infos").contents[3]

# private or public institution
info['type'] = soup.find(
    id="type-etablissement").contents[3].get_text()

# the address
info['address'] = bloc_info.find("div", {"title": "adresse"}).find(
    class_="adresse").get_text()

# phone numbers (list)
info['phone numbers'] = contact_scraper("telephone")

# emails (list)
info['emails'] = contact_scraper("email")

# facebook
facebook_link = bloc_info.find(
    'span', {"class": "fa-facebook"}).find_next_sibling().contents[0]
info['facebook'] = get_link(facebook_link)

# website
website_link = bloc_info.find('span', {"class": "site-web"}).find("a")
info['website'] = get_link(website_link)


# saving to json
with open('schools.json', encoding="utf-8") as f:
    data = json.load(f)
    data['institutes'].append(info)
    print(data)

with open('schools.json', 'w', encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
