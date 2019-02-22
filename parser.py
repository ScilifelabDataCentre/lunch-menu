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
import io
import sys

import PyPDF2
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
    text = text.replace('Ã', '&Aring')
    text = text.replace('â', '&mdash;')
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
def parse_bikupan(resdata, prefix="", suffix=""):
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
        lines.append(prefix + dish.get_text().strip().replace('\n', ' ') + suffix)
    lines += restaurant_end()
    return lines


def parse_dufva(resdata, prefix="", suffix=""):
    '''
    Parse the menu of Sven Dufva
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Uppsala',
                              resdata[2], resdata[4])

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')

    soup = BeautifulSoup(page_req.text, 'html.parser')
    relevant = soup.find("div", {"id": "post"})
    menu_lines = relevant.get_text().split('\n')
    dag = get_weekday()
    started = False
    for line in menu_lines:
        if not line:
            continue
        if line.lower() == dag:
            started = True
            continue
        if started:
            if line[0] != '-':
                lines.append(prefix + line.strip()  + suffix)
            else:
                break
    lines += restaurant_end()
    return lines


def parse_glada(resdata, prefix="", suffix=""):
    '''
    Parse the menu of Glada restaurangen
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    # No way I'll parse this one. If anyone actually wants to, I'd be happy to accept a patch.

    lines += restaurant_end()
    return lines


def parse_haga(resdata, prefix="", suffix=""):
    '''
    Print a link to the menu of Haga gatukök
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])
    lines += restaurant_end()
    return lines


def parse_hjulet(resdata, prefix="", suffix=""):
    '''
    Parse the menu of Restaurang Hjulet
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])
    try:
        page_req = requests.get(resdata[3])
        if page_req.status_code != 200:
            raise IOError('Bad HTTP responce code')

        soup = BeautifulSoup(page_req.text, 'html.parser')
        days = soup.find('table', {'class':'table lunch_menu animation'})
        dishes = days.find('td', {'class':'td_title'})
        lines.append(prefix + dishes.get_text().strip().replace('\n', suffix+'\n'+prefix))
    except Exception as err:
        sys.stderr.write(err)
    lines += restaurant_end()

    return lines


def parse_hubben(resdata, prefix="", suffix=""):
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
        lines.append(prefix + dish.get_text().strip().replace('\n', ' ') + suffix)
    lines += restaurant_end()
    return lines


def parse_jons(resdata, prefix="", suffix=""):
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
    day = days.find('tbody', {'class':'lunch-day-content'})
    dishes = day.find_all('td', {'class':'td_title'})
    for dish in dishes:
        lines.append(prefix + dish.get_text().strip().split('\n')[1] + suffix)

    lines += restaurant_end()
    return lines


def parse_jorpes(resdata, prefix="", suffix=""):
    '''
    Parse the menu of Resturang Jorpes
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])
    lines += restaurant_end()
    return lines


def parse_karolina(resdata, prefix="", suffix=""):
    '''
    Parse the menu of Restaurang Karolina
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    try:
        page_req = requests.get(resdata[3] + f'Meny vecka {get_week()}.pdf')
        if page_req.status_code != 200:
            raise IOError('Bad HTTP responce code')

        kpdf = PyPDF2.PdfFileReader(io.BytesIO(page_req.content))
        text = kpdf.getPage(0).extractText().split('\n')
        digit = -1
        for line in text:
            if 'TRADITIONELL' in line:
                digit += 1
            if digit == get_weekdigit():
                lines.append(prefix + line)
                if not line.isupper():
                    lines[-1] += suffix
                
    except Exception as err:
        sys.stderr.write(str(err) + '\n')

    lines += restaurant_end()
    return lines


def parse_livet(resdata, prefix="", suffix=""):
    '''
    Parse the menu of Livet [restaurant]
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    try:
        page_req = requests.get(resdata[3])
        if page_req.status_code != 200:
            raise IOError('Bad HTTP responce code')

        soup = BeautifulSoup(page_req.text, 'html.parser')
        days = soup.find('div', {'class':'property--xhtml-string'})
        started = False
        for row in days.find_all('p'):
            if get_weekday() in row.get_text().lower():
                started = True
                continue
            if get_weekday(tomorrow=True) in row.get_text().lower():
                break
            if started:
                dish = row.find('b')
                dish_text = dish.get_text().replace('\xa0', '')
                if dish_text:
                    lines.append(prefix + dish_text + suffix)


    except Exception as err:
        sys.stderr.write('E: Livet: {}'.format(err))

    lines += restaurant_end()
    return lines


def parse_mollan(resdata, prefix="", suffix=""):
    '''
    Parse the menu of Mollan
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    # To be fixed some day. Not fun.
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')
    soup = BeautifulSoup(page_req.text, 'html.parser')
    relevant = soup.find_all('span', {'class': 'mobile-undersized-upper'})
    wday = fix_for_html(get_weekday())
    started = False
    for tag in relevant:
        if 'bold' in tag['style']:
            if wday in tag.get_text().lower():
                started = True
                continue
            if started:
                break
        if started:
            lines.append(prefix + fix_for_html(tag.get_text()) + suffix)

    lines += restaurant_end()

    return lines


def parse_nanna(resdata, prefix="", suffix=""):
    '''
    Parse the menu of Nanna Svartz
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])

    # will fix some day. Not fun.
    #page_req = requests.get(resdata[3])
    #if page_req.status_code != 200:
    #    raise IOError('Bad HTTP responce code')

    lines += restaurant_end()
    return lines


def parse_rudbeck(resdata, prefix="", suffix=""):
    '''
    Parse the menu of Bistro Rudbeck
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Uppsala',
                              resdata[2], resdata[4])

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200:
        raise IOError('Bad HTTP responce code')

    soup = BeautifulSoup(page_req.text, 'html.parser')
    days = soup.find_all('div', {'class':'container-fluid no-print'})
    day = days[get_weekdigit()]
    dishes = day.find_all('span')[3:]
    for dish in dishes:
        lines.append(prefix + dish.get_text().strip() + suffix)

    lines += restaurant_end()
    return lines


def parse_subway(resdata, prefix="", suffix=""):
    '''
    Print info about Subway
    '''
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna',
                              resdata[2], resdata[4])
    lines += restaurant_end()
    return lines


def parse_svarta(resdata, prefix="", suffix=""):
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

def restaurant_start(restaurant, location, home_url, mapurl):
    ''''
    Start the listing of the menu of a restaurant
    '''
    return ["""
    <!--{rest}-->
    <div class="title"><a href="{url}">{rest}</a> (<a href="{murl}">{loc}</a>)</div>
    <div class="menu">
      <p>""".format(rest=restaurant, url=home_url, loc=location, murl=mapurl)]


def restaurant_end():
    '''
    Finish the tags after the listing of the menu of a restaurant
    '''
    return ["""      </p>
    </div>"""]
