#!/usr/bin/env python3

# Copyright (c) 2014-2015, Linus Östberg
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

import codecs
from datetime import date
import string
import requests
import sys

from bs4 import BeautifulSoup

class Restaurant() :
    def __init__(self) :
        pass
    def parseToday(self) :
        pass

def fix_for_html(text) :
    '''HTML formatting of characters'''
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
    # MF does for sure not know how to work with text encodings
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
def get_day() :
    return date.today().day

def get_monthdigit() :
    return date.today().month

def get_month() :
    MONTHS = {1: 'januari', 2: 'februari', 3: 'mars', 4: 'april',
              5: 'maj', 6: 'juni', 7: 'juli', 8: 'augusti',
              9: 'september', 10: 'oktober', 11: 'november', 12: 'december'}
    return MONTHS[get_monthdigit()]

def get_weekdigit() :
    return date.today().weekday()

def get_week() :
    return date.today().isocalendar()[1]

def get_weekday(lang = 'sv', tomorrow = False) :
    wdigit = get_weekdigit()
    if tomorrow :
        wdigit += 1
    if lang == 'sv' :
        WEEKDAYS = {0: 'måndag', 1: 'tisdag', 2: 'onsdag', 3: 'torsdag', 
                    4: 'fredag', 5: 'lördag', 6: 'söndag', 7: 'måndag'}
    if lang == 'en' :
        WEEKDAYS = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 
                    4: 'friday', 5: 'saturday', 6: 'sunday', 7: 'monday'}
    return WEEKDAYS[wdigit]
### date management end ###

### parsers start ###
def parse_61an(resdata) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Huddinge', 
                              resdata[3], resdata[4])

    started = False
    title_passed = False
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200 :
        pass # add error logging later

    for line in page_req.text.split('\n') :
        if 'vecka' in line.lower() and not title_passed and not 'meny' in line.lower():
            if not str(week) in line :
                break
            title_passed = True
        if weekday in line.lower() and title_passed :
            started = True
            if tomorrow in line.lower() :
                days = line.split('<STRONG>')
                if len(days) == 1 :
                    days = line.split('<strong>')
                if len(days) == 1 :
                    break
                for d in range(len(days)) :
                    if weekday in days[d].lower() :                        
                        parts = days[d].split('<br />')
                        if len(parts) == 1 :
                            parts = days[d].split('<br>')
                        if len(parts) == 1 :
                            break
                        for i in range(1, len(parts), 1) :
                            if len(fix_for_html(remove_html(parts[i]))) > 0 :
                                lines.append(fix_for_html(remove_html(parts[i]) + '<br/>'))
        if not started :
            continue
        if tomorrow in line.lower() or 'streck2.gif' in line or len(line.strip()) < 25 :
            break
        tmp = line.strip()
        tmp = tmp[tmp.lower().index(weekday) + len(weekday):]
        parts = tmp.split('<BR>')
        for i in range(1, len(parts), 1) :
            lines.append(fix_for_html(remove_html(parts[i]) + '<br/>'))

    lines += restaurant_end()
    return lines

def parse_alfred(resdata) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Huddinge', 
                              resdata[3], resdata[4])

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200 :
        pass # add error logging later
    soup = BeautifulSoup(page_req.text, 'html.parser')

    try :
        menu = soup.find_all('div')[85]

        wdigit = get_weekdigit()
        if wdigit < 5 :
            base = 3 + 7*wdigit
            for i in range(4) :
                lines.append(fix_for_html(remove_html(str(menu.find_all('p')[base + i]))) + '<br/>')
                
    except :
        pass
        
    lines += restaurant_end()

    return lines

def parse_glada(resdata) :
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Huddinge', 
                              resdata[3], resdata[4])

    week = get_week()
    tomorrow = get_weekday(tomorrow=True)
    today = get_weekday()

    menu_reached = False
    start = False
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200 :
        pass # add error logging later
    for line in page_req.text.split('\n') :
        if 'Vecka' in line and '</h1>' in line :
            if str(week) not in line.lower() :
                pass
            menu_reached = True
        if menu_reached and today in line.lower() :
            start = True
            continue
        if not start :
            continue
        if tomorrow in line.lower()  or 'i samtliga rätter ingår' in line.lower() :
            break
        if not '<em>' in line and not '<p>Vegetariskt<br />' in line :
            # remove seperate lines for e.g. "Pasta"
            if len(remove_html(line).split(' ')) > 1 :
                lines.append(fix_for_html(remove_html(line.strip())) + '<br/>')
        
    lines += restaurant_end()
    return lines

def parse_haga(resdata) :
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna', 
                              resdata[3], resdata[4])
    lines += restaurant_end()
    return lines
    
def parse_hjulet(resdata) :
    day = get_day()
    month = get_month()
    today = get_weekday()

    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna', 
                              resdata[3], resdata[4])

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200 :
        pass # add error logging later

    soup = BeautifulSoup(page_req.text, 'html.parser')

    # find the weekday index
    day_index = None
    i = 0
    try :
        for header in soup.find_all('table')[0].find_all('th') :
            if today in str(header).lower() and str(day) in str(header).lower() and month in str(header).lower() :
                day_index = i
            i += 1
        if day_index != None :
            menu = soup.find_all('table')[0].find_all('td')[day_index*15:(day_index+1)*15:3]
            for i in range(len(menu)) :
                menu[i] = fix_for_html(remove_html(str(menu[i])))
                if len(menu[i].strip()) > 0 :
                    lines.append(menu[i] + '<br/>')
        else :
            pass
    except Exception as err :
        pass
    lines += restaurant_end()

    return lines

def parse_jons(resdata) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    day = get_day()
    month = get_month()
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna', 
                              resdata[3], resdata[4])
    
    start = False
    today = '{wday}  {iday} {mon}'.format(wday = weekday, iday = day, mon = month)
    today_alt = '{wday} {iday} {mon}'.format(wday = weekday, iday = day, mon = month)
    current = list()
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200 :
        pass # add error logging later
    for line in page_req.text.split('\n') :
        if today in line.lower() or today_alt in line.lower() :
            start = True
            continue
        if start and (tomorrow in line.lower() or '<!-- contact -->' in line.lower()) :
            break
        if start :
            tmp = fix_for_html(remove_html(line.strip()))
            if len(tmp.strip()) > 0 :
                current.append(tmp.strip())
            if '</tr>' in line :
                if len(current) > 0 :
                    lines.append(' '.join(current) + '<br/>')
                    current = list()

    lines += restaurant_end()
    return lines

def parse_jorpes(resdata) :
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna', 
                              resdata[3], resdata[4])
    lines += restaurant_end()
    return lines


def parse_karolina(resdata) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    day = get_day()
    month = get_month()
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna', 
                              resdata[3], resdata[4])
    
    start = False
    today = '{wday} {iday} {mon}'.format(wday = weekday, iday = day, mon = month)
    today_alt = '{wday}  {iday} {mon}'.format(wday = weekday, iday = day, mon = month)
    current = list()
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200 :
        pass # add error logging later
    for line in page_req.text.split('\n') :
        if today in line.lower() or today_alt in line.lower() :
            start = True
            continue
        if start and (tomorrow in line.lower() or 'gäller hela veckan' in line.lower()) :
            break
        if start :
            tmp = fix_for_html(remove_html(line))
            if len(tmp.strip()) > 0 :
                current.append(tmp.strip())
            if '</tr>' in line :
                if len(current) > 0 :
                    lines.append(' '.join(current) + '<br/>')
                    current = list()

    lines += restaurant_end()
    return lines

def parse_konigs(resdata) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    day = get_day()
    month = get_month()
    
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna', 
                              resdata[3], resdata[4])
    start = False
    menu_passed = False
    
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200 :
        pass # add error logging later
    for line in page_req.text.split('\n') :
        if 'VECKA' in line :
            if str(week) not in line :
                break
        if 'Veckans matsedel:' in line :
            menu_passed = True
            continue

        if menu_passed and (weekday in line.lower() or fix_for_html(weekday) in line.lower()) :
            start = True
            continue
        if not start :
            continue
        if tomorrow in line.lower() or 'Veckans soppa:' in line :
            break
        line = line.replace('<div>', '')
        line = line.replace('</div>', '')
        line = line.replace(' ', '')
        lines.append(fix_for_html(line))

    lines += restaurant_end()

    return lines

def parse_matmakarna(resdata) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Huddinge', 
                              resdata[3], resdata[4])
    rad_checker = False
    started = False
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200 :
        pass # add error logging later
    for line in page_req.text.split('\n') :
        if 'vecka ' in line.lower() and not started and not 'meny' in line.lower():
            if not str(week) in line :
                break
        if weekday.upper() in line and 'START' in line :
            started = True
            continue
        if not started :
            continue
        if weekday.upper() in line and 'SLUT' in line :
            break
        if '<!-- rad' in line.lower() :
            rad_checker = True
            continue
        if rad_checker :
            tmp = remove_html(line).strip()
            if len(tmp) > 0 :
                lines.append(fix_for_html(tmp) + '<br/>')
                rad_checker = False
            else :
                continue
        else :
            continue

    lines += restaurant_end()
    return lines

def parse_mf(resdata) :
    # Funny fact: W3C validator crashes while analysing this page.
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna', 
                              resdata[3], resdata[4])
    if weekday == 'måndag' :
        weekday = 'ndag'

    start = False
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200 :
        pass # add error logging later
    for line in page_req.text.split('\n') :
        if 'meny vecka' in line.lower() :
            if 'veckans' in line.lower() :
                continue
            if not str(week) in line :
                break
        if weekday in line.lower() :
            start = True
            continue
        if tomorrow in line.lower() :
            break
        if 'Pris' in line and start :
            break
        if not start :
            continue
        if len(fix_for_html(remove_html(line)).strip()) == 0 :
            continue
        else : 
            lines.append(fix_for_html(remove_html(line)).strip() + '<br/>')


    lines += restaurant_end()

    return lines

def parse_mollan(resdata) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna', 
                              resdata[3], resdata[4])

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200 :
        pass # add error logging later
    soup = BeautifulSoup(page_req.text, 'html.parser')
    try :
        relevant = soup.find_all('div')[24]
        # check week
        if not str(week) in str(relevant.find_all('div')[0]) :
            pass
        wdigit = get_weekdigit()
        if wdigit < 5 :
            base = 2 + 7*wdigit
            for i in range(6) :
                lines.append(fix_for_html(remove_html(str(relevant.find_all('p')[base + i]))) + '<br/>')
    except :
        pass
            
    lines += restaurant_end()

    return lines

def parse_nanna(resdata) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna', 
                              resdata[3], resdata[4])

    start = False
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200 :
        pass # add error logging later
    for line in page_req.text.split('\n') :
        if 'meny' in line.lower() and 'vecka' in line.lower() :
            if not str(week) in line :
                break
        # looking for the lines where the menu is listed in bold text
        if weekday in line.lower() and 'h3' in line.lower() :
            start = True
            continue
        # alternative formatting
        if weekday in line.lower() and '<strong>' in line.lower() :
            start = True
            continue
        # end of day
        if start and (tomorrow in line.lower() or '<div class="span6">' in line) :
            break
        if start and len(remove_html(line.strip())) > 1 :
            lines.append(fix_for_html(remove_html(line.strip())) + '<br/>')

    lines += restaurant_end()

    return lines

def parse_stories(resdata) :
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Huddinge', 
                              resdata[3], resdata[4])
    lines += restaurant_end()
    return lines

def parse_subway(resdata) :
    wdigit = get_weekdigit()
    # sub of the day
    subotd = {0: 'American Steakhouse Melt', 1: 'Subway Melt', 2: 'Spicy Italian',
              3: 'Rostbiff', 4: 'Tonfisk', 5: 'Subway Club', 6: 'Italian B.M.T-',
              7: 'American Steakhouse Melt'}
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna', 
                              resdata[3], resdata[4])

    lines.append('<p> Sub of the day: {0}</p>\n'.format(fix_for_html(subotd[wdigit])))
    lines += restaurant_end()
    return lines

def parse_svarta(resdata) :
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Solna', 
                              resdata[3], resdata[4])
    lines += restaurant_end()
    return lines

def parse_tango(resdata) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    day = get_day()
    month = get_month()
    lines = list()
    lines += restaurant_start(fix_for_html(resdata[1]), 'Huddinge', 
                              resdata[3], resdata[4])
    
    start = False
    today = '{wday} {iday} {mon}'.format(wday = weekday, iday = day, mon = month)
    today_alt = '{wday}  {iday} {mon}'.format(wday = weekday, iday = day, mon = month)

    page_req = requests.get(resdata[3])
    if page_req.status_code != 200 :
        pass # add error logging later
    for line in page_req.text.split('\n') :
        if today in line.lower() or today_alt in line.lower() :
            start = True
            continue
        if start and (tomorrow in line.lower() or 'gäller hela veckan' in line.lower()) :
            break
        if start :
            tmp = fix_for_html(remove_html(line))
            if len(tmp.strip()) > 4 : # get rid of the line with pricing
                lines.append(tmp.strip() + '<br/>')

    lines += restaurant_end()
    return lines
### parsers end ###

def remove_html(text) :
    text = text.replace('&nbsp;', ' ')
    # assumes all < are part of html tags
    try :
        for i in range(0, text.count('<')) :
                text = text[:text.index('<')] + text[text.index('>')+1:]
    except :
        pass
    return text

def restaurant_end() :
    lines = list()
    lines.append('</p>')
    lines.append('</div>')
    return lines

def restaurant_start(restaurant, location, home_url, mapurl) :
    lines = list()
    lines.append('<!--{}-->'.format(restaurant))
    lines.append('''<div class="title"><a href="{url}"> {rest}</a> (<a href="{murl}">{loc}</a>)</div>'''.format(rest = restaurant, 
                                                                                                                url = home_url, 
                                                                                                                loc = location,
                                                                                                                murl = mapurl))
    lines.append('<div class="menu">')
    lines.append('<p>')
    return lines
