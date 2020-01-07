#!/usr/bin/env python3

# Copyright (c) 2014-2020, Linus Östberg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of kimenu nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
Parsers of the menu pages for the restaurants at Karolinska Institutet
'''

from datetime import date
import re

import requests
from bs4 import BeautifulSoup


def restaurant(func):
    """
    Decorator to use for restaurants.
    """
    def helper(res_data):
        data = {'title': res_data['name'],
                'location': res_data['campus'],
                'url': res_data['url'],
                'map_url': res_data['osm']}
        data.update(func(res_data))
        return data
    helper.__name__ = func.__name__
    helper.__doc__ = func.__doc__

    return helper


def get_parser(url: str) -> BeautifulSoup:
    """
    Request page and create Beautifulsoup object
    """
    page_req = requests.get(url)
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')

    return BeautifulSoup(page_req.text, 'html.parser')


def fix_bad_symbols(text):
    '''
    HTML formatting of characters
    '''
    text = text.replace('Ã¨', 'è')
    text = text.replace('Ã¤', 'ä')
    text = text.replace('Ã', 'Ä')
    text = text.replace('Ã', 'Ä')
    text = text.replace('Ã¶', 'ö')
    text = text.replace('Ã©', 'é')
    text = text.replace('Ã¥', 'å')
    text = text.replace('Ã', 'Å')

    text = text.strip()

    return text


### date management start ###
def get_day():
    '''
    Today as digit
    '''
    return date.today().day


def get_monthdigit():
    '''
    Month as digit
    '''
    return date.today().month


def get_month():
    '''
    Month name
    '''
    months = {1: 'januari', 2: 'februari', 3: 'mars', 4: 'april',
              5: 'maj', 6: 'juni', 7: 'juli', 8: 'augusti',
              9: 'september', 10: 'oktober', 11: 'november', 12: 'december'}

    return months[get_monthdigit()]


def get_week():
    '''
    Week number
    '''
    return date.today().isocalendar()[1]


def get_weekday(lang='sv', tomorrow=False):
    '''
    Day name in swedish(sv) or english (en)
    '''
    wdigit = get_weekdigit()
    if tomorrow:
        wdigit += 1
    if lang == 'sv':
        weekdays = {0: 'måndag', 1: 'tisdag', 2: 'onsdag', 3: 'torsdag',
                    4: 'fredag', 5: 'lördag', 6: 'söndag', 7: 'måndag'}
    if lang == 'en':
        weekdays = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday',
                    4: 'friday', 5: 'saturday', 6: 'sunday', 7: 'monday'}
    return weekdays[wdigit]


def get_weekdigit():
    '''
    Get digit for week (monday = 0)
    '''
    return date.today().weekday()


def get_year():
    '''
    Year as number
    '''
    return date.today().year
### date management end ###

### parsers start ###
@restaurant
def parse_bikupan(res_data: dict) -> dict:
    '''
    Parse the menu of Restaurang Bikupan
    '''
    data = {'menu': []}
    soup = get_parser(res_data['menu_url'])
    relevant = soup.find("div", {"class": "col-md-3 hors-menu text-center"})
    dishes = relevant.find_all("div", {"class": "col-xs-10 text-left"})
    for dish in dishes:
        data['menu'].append(dish.get_text().strip().replace('\n', ' '))
    return data


@restaurant
def parse_dufva(res_data):
    '''
    Parse the menu of Sven Dufva
    '''
    data = {'menu': []}
    soup = get_parser(res_data['menu_url'])

    relevant = soup.find("div", {"id": "post"})
    menu_data = relevant.get_text().split('\n')
    dag = get_weekday()
    started = False
    for line in menu_data:
        if not line:
            continue
        if line.lower() == dag:
            started = True
            continue
        if started:
            if line[0] != '-':
                data['menu'].append(line.strip())
            else:
                break
    return data


@restaurant
def parse_glada(res_data):
    '''
    Parse the menu of Glada restaurangen
    '''
    data = {'menu': []}
    # No way I'll parse this one. If anyone actually wants to, I'd be happy to accept a patch.
    return data


@restaurant
def parse_haga(res_data):
    '''
    Print a link to the menu of Haga gatukök
    '''
    return {'menu': []}


@restaurant
def parse_hjulet(res_data):
    '''
    Parse the menu of Restaurang Hjulet
    '''
    data = {'menu': []}
    soup = get_parser(res_data['menu_url'])

    for header in soup.find_all('h4'):
        if header.find(text=re.compile('LUNCH MENY')) and str(get_week()) in header.text:
            # Will fail if the day is in a non-menu paragraph
            for par in soup.find_all('p'):
                if par.find(text=re.compile('^' + get_weekday().capitalize())):
                    data['menu'] += par.text.split('\n')[1:]
                    break

    return data


@restaurant
def parse_hubben(res_data):
    '''
    Parse the menu of Restaurang Hubben
    '''
    data = {'menu': []}
    soup = get_parser(res_data['menu_url'])

    days = soup.find_all("div", {"class": "day"})
    current = days[get_weekdigit()]
    dishes = current.find_all('div', {'class': 'element description col-md-4 col-print-5'})
    for dish in dishes:
        data['menu'].append(dish.get_text().strip().replace('\n', ' '))

    return data


@restaurant
def parse_jons(res_data):
    '''
    Parse the menu of Jöns Jacob
    '''
    data = {'menu': []}
    soup = get_parser(res_data['menu_url'])

    days = soup.find('table', {'class':'table lunch_menu animation'})
    day = days.find('tbody', {'class':'lunch-day-content'})
    dishes = day.find_all('td', {'class':'td_title'})
    for dish in dishes:
        dish_data = ' '.join([text for text in dish.get_text().strip().split('\n')[1:] if text])
        if dish_data:
            data['menu'].append(dish_data)

    return data


@restaurant
def parse_jorpes(res_data):
    '''
    Parse the menu of Resturang Jorpes
    '''
    data = {'menu': []}
    return data


@restaurant
def parse_livet(res_data):
    '''
    Parse the menu of Livet
    '''
    data = {'menu': []}
    soup = get_parser(res_data['menu_url'])

    started = False
    for par in soup.find_all(('h3', 'p')):
        if started:
            if par.find(text=re.compile(get_weekday(tomorrow=True).capitalize())):
                break
            if par.find(text=re.compile('[Pp]ersonuppgifterna')):
                break
            text = par.find(text=True, recursive=False)
            if text:
                data['menu'].append(text)
            continue
        if par.find(text=re.compile(get_weekday().capitalize() +
                                    '.*' +
                                    str(get_day()))):
            started = True

    return data


@restaurant
def parse_mollan(res_data):
    '''
    Parse the menu of Mollan
    '''
    data = {'menu': []}
    soup = get_parser(res_data['menu_url'])

    current_week = False
    for span in soup.find_all('span'):
        if span.find(text=re.compile('Vecka.*' + str(get_week()))):
            current_week = True

    if current_week:
        days = soup.find_all('ol')
        today = days[get_weekdigit()]
        for entry in [fix_bad_symbols(entry.text) for entry in today.find_all('li')]:
            data['menu'].append(entry)


    return data


@restaurant
def parse_nanna(res_data):
    '''
    Parse the menu of Nanna Svartz
    '''
    data = {'menu': []}
    soup = get_parser(res_data['menu_url'])

    current_week = False
    for tag in soup.find_all('strong'):
        if tag.find(text=re.compile(r'MATSEDEL V\.' + str(get_week()))):
            current_week = True

    if current_week:
        started = False
        for par in soup.find_all('p'):
            if started:
                if (par.find(text=re.compile(get_weekday(tomorrow=True).capitalize())) or
                    par.find(text=re.compile(r'^Priser'))):
                    break
                dish_parts = [text for text in par.text.replace('\xa0', '').strip().split(' ')
                              if text]
                if dish_parts and dish_parts[0] in ('Vegetarisk', 'Kött', 'Sallad', 'Fisk'):
                    dish_text = ' '.join(dish_parts[1:])
                    if dish_text:
                        data['menu'].append(dish_text)
            if par.find(text=re.compile(get_weekday().capitalize())):
                started = True

    return data


@restaurant
def parse_rudbeck(res_data):
    '''
    Parse the menu of Bistro Rudbeck
    '''
    data = {'menu': []}
    soup = get_parser(res_data['menu_url'])

    days = soup.find_all('div', {'class':'container-fluid no-print'})
    day = days[get_weekdigit()]
    dishes = day.find_all('span')[3:]
    for dish in dishes:
        data['menu'].append(dish.get_text().strip())

    return data


@restaurant
def parse_svarta(res_data):
    '''
    Parse the menu of Svarta Räfven
    '''
    return {'menu': []}
