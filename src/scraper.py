from os import major
from sys import stderr
from types import resolve_bases
from typing import List
import requests
from bs4 import BeautifulSoup
from sqlalchemy.sql.sqltypes import String
from datetime import datetime

event_url = 'http://ufcstats.com/event-details/2f13e4020cea5b38'
base_page = 'http://ufcstats.com/statistics/events/completed?page=all'


def extract_pages(base_url: String):
    # TODO: Fix this, hacky. Returns a list of tuples, the link for the page and the date the event ocurred
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, "html.parser")
    sections = soup.find_all(class_='b-statistics__table-content')
    date_strings = soup.find_all(class_="b-statistics__date")
    links = []
    for section in sections:
        links.append(section.find("a").get('href'))
    # Top link will be next upcoming event which will not contain results,
    # discard it
    links = links[1:]
    date_strings = date_strings[1:]
    dates_converted = map(lambda x: datetime.strptime(x.text.strip(), '%B %d, %Y').date(), date_strings)
    zipped_list = list(zip(links, dates_converted))
    return zipped_list

def extract_bouts(soup, date):
    results = soup.find_all(class_="b-fight-details__table-row")
    results = results[1:len(results)]
    bouts = []
    outcome = ""
    for item in results:
        try:
            is_draw = item.find(class_="b-flag__text").text.strip() == "draw"
            winner = item.find(class_="b-link").text.strip()
            loser = item.find_all(class_="b-link")[1].text.strip()
            weight_class = item.find_all("td")[6].text.strip()
            outcome = item.find_all("td")[7].text.strip()
            major_outcome = outcome.split()[0]
            minor_outcome = ' '.join(outcome.split()[1:]) if len(outcome.split()) else ""
            bout = { 'winner': winner, 'loser': loser, 
                'weight_class': weight_class, 'major_outcome' : major_outcome,
                'minor_outcome': minor_outcome, 'is_draw': is_draw,
                'bout_date': date }
            bouts.append(bout)
        except Exception as e:
            print(item, file = stderr)
    return bouts

def print_bouts(bouts: List):
    for bout in bouts:
        if not bout['is_draw']:
            print(f'{bout["winner"]} defeats {bout["loser"]} at {bout["weight_class"]} via {bout["major_outcome"]} on {bout["bout_date"]}')
        else:
            print(f'Draw between {bout["winner"]} and {bout["loser"]} at {bout["weight_class"]} via {bout["major_outcome"]} on {bout["bout_date"]}')

def fetch_bouts():
    bouts = []
    link_date_touples = extract_pages(base_page)
    for touple in link_date_touples:
        link = touple[0]
        date = touple[1]
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        page_bouts = extract_bouts(soup, date)
        bouts.extend(page_bouts)
    return bouts


