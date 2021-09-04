from os import major
from types import resolve_bases
import requests
from bs4 import BeautifulSoup
import psycopg2

event_url = 'http://ufcstats.com/event-details/2f13e4020cea5b38'
base_page = 'http://ufcstats.com/statistics/events/completed?page=all'


def extract_pages(base_url):
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, "html.parser")
    sections = soup.find_all(class_='b-statistics__table-content')
    links = []
    for section in sections:
        links.append(section.find("a").get('href'))
    links = links[1:]
    return links

# def extract_bouts(soup):
#     results = soup.find_all(class_="b-fight-details__table-row")
#     results = results[1:len(results)]
#     bouts = []
#     outcome = ""
#     for item in results:
#         winner = item.find(class_="b-link").text.strip()
#         loser = item.find_all(class_="b-link")[1].text.strip()
#         weight_class = item.find_all("td")[6].text.strip()
#         outcome = item.find_all("td")[7].text.strip()
#         major_outcome = outcome.split()[0]
#         minor_outcome = ' '.join(outcome.split()[1:]) if len(outcome.split()) else ""
#         bout = { 'winner': winner, 'loser': loser, 'weight_class': weight_class, 'major_outcome' : major_outcome, 'minor_outcome': minor_outcome}
#         bouts.append(bout)
#     return bouts

# bouts = []
# links = extract_pages(base_page)
# for link in links:
#     page = requests.get(link)
#     soup = BeautifulSoup(page.content, "html.parser")
#     page_bouts = extract_bouts(soup)
#     bouts.extend(page_bouts)

conn = psycopg2.connect(host="localhost", port = 5432, user="postgres", password="")
cur = conn.cursor()
cur.execute("""SELECT datname FROM pg_database;""")
print(cur.fetchall())

# for bout in bouts:
#     print(f'{bout["winner"]} defeats {bout["loser"]} at {bout["weight_class"]} via {bout["major_outcome"]}')

