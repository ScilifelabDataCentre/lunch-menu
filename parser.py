#!/usr/bin/env python3

# Copyright (c) 2014-2018, Linus Östberg
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

import requests
from bs4 import BeautifulSoup


def fix_for_html(text):
    '''
    HTML formatting of characters
    '''
    text = text.replace('ö', '&ouml;')
    text = text.replace('Ö', '&Ouml;')
    text = text.replace('å', '&aring;')
    text = text.replace('Å', '&Aring;')
    text = text.replace('ä', '&auml;')
    text = text.replace('Ä', '&Auml;')
    text = text.replace('é', '&eacute;')
    text = text.replace('è', '&egrave;')
    text = text.replace('í', '&iacute;')
    text = text.replace('ì', '&igrave;')
    text = text.replace('à', '&agrave;')
    text = text.replace('á', '&aacute;')
    text = text.replace('ô', '&ocirc;')
    text = text.replace('ü', '&uuml;')
    text = text.replace('Ä', '&Auml;')
    text = text.replace('´', '&#39;')
    text = text.replace('`', '&#39;')
    text = text.replace('ç', '&ccedil;')
    text = text.replace('”', '&quot;')
    text = text.replace('Ã¨', '&egrave;')
    text = text.replace('Ã¤', '&auml;')
    text = text.replace('Ã', '&Auml;')
    text = text.replace('Ã', '&Auml;')
    text = text.replace('Ã¶', '&ouml;')
    text = text.replace('Ã©', '&eacute;')
    text = text.replace('Ã¥', '&aring;')
    text = text.replace(' ', '')
    text = text.replace('Ã', '&Aring')
    # Karolina
    text = text.replace('å', '&aring;')
    text = text.replace('ä', '&auml;')
    text = text.replace('ö', '&ouml;')
    text = text.replace('Ä', '&Auml;')

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
    return date.today().weekday()


def get_year():
    '''
    Year as number
    '''
    return date.today().year
### date management end ###

### parsers start ###
def parse_bikupan(resdata):
    '''
    Parse the menu of Restaurang Bikupan
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Uppsala',
                              resdata[2], resdata[4])

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')

    soup = BeautifulSoup(page_req.text, 'html.parser')
    relevant = soup.find("div", {"class": "col-md-3 hors-menu text-center"})
    dishes = relevant.find_all("div", {"class": "col-xs-10 text-left"})
    for dish in dishes:
        lines.append(dish.get_text().strip().replace('\n', ' ') + '<br/>')
    lines += restaurant_end()
    return lines


def parse_glada(resdata):
    '''
    Parse the menu of Glada restaurangen
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    # No way I'll parse this one. If anyone actually wants to, I'd be happy to accept a patch.

    lines += restaurant_end()
    return lines


def parse_haga(resdata):
    '''
    Print a link to the menu of Haga gatukök
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])
    lines += restaurant_end()
    return lines


def parse_hjulet(resdata):
    '''
    Parse the menu of Restaurang Hjulet
    '''
    day = get_day()
    month = get_month()
    today = get_weekday()

    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')

    soup = BeautifulSoup(page_req.text, 'html.parser')
    days = soup.find('table', {'class':'table lunch_menu animation'})
    # they seem to remove all old days, keeping today as [0]; must be confirmed
    dishes = days.find('td', {'class':'td_title'})
    lines.append(dishes.get_text().strip().replace('\n', '<br/>'))
    lines += restaurant_end()

    return lines


def parse_hubben(resdata):
    '''
    Parse the menu of Restaurang Hubben
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Uppsala',
                              resdata[2], resdata[4])

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')

    soup = BeautifulSoup(page_req.text, 'html.parser')
    days = soup.find_all("div", {"class": "day"})
    current = days[get_weekdigit()]
    dishes = current.find_all('div', {'class': 'element description col-md-4 col-print-5'})
    for dish in dishes:
        lines.append(dish.get_text().strip().replace('\n', ' ') + '<br/>')
    lines += restaurant_end()
    return lines


def parse_jons(resdata):
    '''
    Parse the menu of Jöns Jacob
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')

    soup = BeautifulSoup(page_req.text, 'html.parser')
    days = soup.find('table', {'class':'table lunch_menu animation'})
    # they seem to remove all old days, keeping today as [0]; must be confirmed
    day = days.find('tbody', {'class':'lunch-day-content'})
    dishes = day.find_all('td', {'class':'td_title'})
    for dish in dishes:
        lines.append(dish.get_text().strip().split('\n')[1] + '<br/>')

    lines += restaurant_end()
    return lines


def parse_jorpes(resdata):
    '''
    Parse the menu of Resturang Jorpes
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])
    lines += restaurant_end()
    return lines


def parse_karolina(resdata):
    '''
    Parse the menu of Restaurang Karolina
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')

    soup = BeautifulSoup(page_req.text, 'html.parser')
    days = soup.find('table', {'class':'table lunch_menu animation'})
    # they seem to remove all old days, keeping today as [0]; must be confirmed
    day = days.find('tbody', {'class':'lunch-day-content'})
    dishes = day.find_all('td', {'class':'td_title'})
    for dish in dishes:
        lines.append(dish.get_text().strip().split(':')[1] + '<br/>')

    lines += restaurant_end()
    return lines


def parse_mollan(resdata):
    '''
    Parse the menu of Mollan
    '''
    week = get_week()

    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    # To be fixed some day. Not fun.
    #page_req = requests.get(resdata[3])
    #if page_req.status_code != 200:
    #    raise IOError('Bad HTTP responce code')
    #soup = BeautifulSoup(page_req.text, 'html.parser')
    
    lines += restaurant_end()

    return lines


def parse_nanna(resdata):
    '''
    Parse the menu of Nanna Svartz
    '''
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow=True)
    week = get_week()

    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    # will fix some day. Not fun.
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')
    
    lines += restaurant_end()
    return lines


def parse_subway(resdata):
    '''
    Print info about Subway
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])
    lines += restaurant_end()
    return lines


def parse_svarta(resdata):
    '''
    Parse the menu of Svarta Räfven
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    # page_req = requests.get(resdata[3])
    # soup = BeautifulSoup(page_req.text, 'html.parser')

    lines += restaurant_end()
    return lines

### parsers end ###

def remove_html(text):
    '''
    Remove HTML tags
    '''
    text = text.replace('&nbsp;', ' ')
    # assumes all < are part of html tags
    try:
        while text.count('<') > 0:
            text = text[:text.index('<')] + text[text.index('>')+1:]
    except:
        pass
    return text


def restaurant_end():
    '''
    Finish the tags after the listing of the menu of a restaurant
    '''
    lines = list()
    lines.append('</p>')
    lines.append('</div>')
    return lines


def restaurant_start(restaurant, location, home_url, mapurl):
    ''''
    Start the listing of the menu of a restaurant
    '''
    lines = list()
    lines.append('<!--{}-->'.format(restaurant))
    lines.append('''<div class="title"><a href="{url}"> {rest}</a> (<a href="{murl}">{loc}</a>)</div>'''.format(rest=restaurant,
                                                                                                                url=home_url,
                                                                                                                loc=location,
                                                                                                                murl=mapurl))
    lines.append('<div class="menu">')
    lines.append('<p>')
    return lines
