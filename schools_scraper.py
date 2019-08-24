import requests
from bs4 import BeautifulSoup
import json


def contact_scraper(selector):
    contact = bloc_info.find(class_=selector)
    contact_list = []

    if contact:
        contact_list.append(contact.get_text())
    else:
        return ''

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


def scraping():
    info = {}

    name = soup.find(class_="denomination").get_text()

    city = soup.find(class_="fa-map-marker").find_next_sibling().text
    city = city[0:10]

    if city == "Casablanca":

        # get the name
        info['name'] = name

        # get the logo
        logo = soup.find('img', {"class": "img-container"})["src"]
        logo = "http://www.ecolia.ma{}".format(logo[2:])

        if logo != 'http://www.ecolia.ma/annuaire/logo/logo-v2.png':
            info['logo'] = logo
        else:
            info['logo'] = ''

        # Levels
        levels = []
        all_levels = soup.select(".entite-existe")
        for level in all_levels:
            levels.append(level.contents[0].text)

        info["levels"] = levels

        # private or public institution
        info['type'] = soup.find(
            id="type-etablissement").contents[3].get_text()

        # the address
        info['address'] = bloc_info.find("div", {"title": "adresse"}).find(
            class_="adresse").get_text()

        # director
        director = soup.find(class_="directeur").text

        if director.lstrip() != "Cliquer pour remplir":
            info['director'] = director

        # phone numbers (list)
        info['phone numbers'] = contact_scraper("telephone")

        # emails (list)
        info['emails'] = contact_scraper("email")

        # facebook
        try:
            facebook_link = bloc_info.find(
                'span', {"class": "fa-facebook"}).find_next_sibling().contents[0]
            info['facebook'] = get_link(facebook_link)
        except AttributeError:
            facebook_link = ''

        # website
        try:
            website_link = bloc_info.find(
                'span', {"class": "site-web"}).find("a")
            info['website'] = get_link(website_link)
        except AttributeError:
            website_link = ''

    # saving to json
        with open('schools.json',  encoding="utf-8") as f:
            data = json.load(f)
            data['institutes'].append(info)

        with open('schools.json', 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def get_urls(page):
    response = requests.get(page)
    bsoup = BeautifulSoup(response.text, "html.parser")

    tags = bsoup.find(id="list-ecole-content").select("h3")
    urls = set()

    for h3 in tags:
        urls.add("http://www.ecolia.ma/{}".format(h3.contents[0]['href']))

    return urls


# main
urls = set()
for i in range(2, 100):
    new_urls = get_urls("http://www.ecolia.ma/ecoles-page-{}".format(i))
    urls.update(new_urls)


for url in urls:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    bloc_info = soup.find(class_="ecole-bloc-infos").contents[3]

    scraping()
