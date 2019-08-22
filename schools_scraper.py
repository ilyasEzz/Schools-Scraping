import requests
from bs4 import BeautifulSoup
import csv


url = 'http://www.ecolia.ma/ecole-maternelle-du-groupe-scolaire-de-la-residence-3-674'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


def contact_scraper(selector):
    contact = infos.find(class_=selector)
    contact_list = []
    contact_list.append(contact.get_text().encode("utf-8"))

    # other contact infos
    if contact.find_parent().find("ul", {"class": "dropdown"}):

        for item in contact.find_parent().select("ul", {"class": "dropdown"}):
            for other_nums in item.select("li"):
                if other_nums.get_text() != ' ':
                    contact_list.append(other_nums.get_text().encode("utf-8"))

    return contact_list


def get_link(a):
    if a.text != 'Cliquer pour remplir':
        return a["href"]
    else:
        return ''


with open('schools.csv', 'w') as csv_file:
    # get the name
    name = soup.find(class_="denomination").get_text().encode("utf-8")

    # Levels
    levels = ''
    all_levels = soup.select(".entite-existe")
    for label in all_levels:
        levels = "{}, {}".format(levels, label.find(
            "span").get_text()).encode("utf-8")

    # bloc with the main information
    infos = soup.find(class_="ecole-bloc-infos").contents[3]

    # private or public institution
    cost = soup.find(
        id="type-etablissement").contents[3].get_text().encode("utf-8")

    # the address
    address = infos.find("div", {"title": "adresse"}).find(
        class_="adresse").get_text().encode("utf-8")

    # phone numbers (list)
    phone_numbers = contact_scraper("telephone")

    # emails (list)
    emails = contact_scraper("email")

    # facebook
    facebook_link = infos.find(
        'span', {"class": "fa-facebook"}).find_next_sibling().contents[0]

    facebook = get_link(facebook_link).encode("utf-8")

    # website
    website_link = infos.find('span', {"class": "site-web"}).find("a")
    website = get_link(website_link).encode("utf-8")

    # csv
    csv_writer = csv.writer(csv_file)
    headers = ["name", "address", "type", "cost",
               "phone numbers", "emails", "facebook", "website"]
    csv_writer.writerow(headers)
    csv_writer.writerow([name, address, cost, levels,
                         phone_numbers, emails, phone_numbers, facebook, website])
