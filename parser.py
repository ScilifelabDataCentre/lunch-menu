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
def parse_konigs(resdata) :
    # [0] identifier [1] Name [2] URL [3] Menu URL [4] OSM URL
    page_req = requests.get(resdata[3])
    if page_req.status_code != 200 :
        pass # add error logging later
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
