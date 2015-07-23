#!/usr/bin/env python3

# Copyright (c) 2014, Linus Östberg
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
import sys

from bs4 import BeautifulSoup


DEBUG = True

def error(text) :
    if DEBUG :
        sys.stderr.write('ERROR: ' + text + '\n')

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

def get_day() :
    return date.today().day

def get_monthdigit() :
    return date.today().month

def get_month() :
    MONTHS = {1: 'januari', 2: 'februari', 3: 'mars', 4: 'april', 5: 'maj', 6: 'juni',
              7: 'juli', 8: 'augusti', 9: 'september', 10: 'oktober', 11: 'november', 12: 'december'}
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

def note(text) :
    if DEBUG :
        sys.stderr.write('NOTE: ' + text + '\n')


def page_end() :
    lines = list()
    lines.append('<div class="endnote">Code available at <a href="https://github.com/talavis/kimenu">Github</a>. Patches are very welcome.</div>')
    lines.append('</body>')
    lines.append('</html>')
    return lines

def page_start(weekday, day, month) :
    lines = list()
    lines.append('<html>')
    lines.append('<head>')
    lines.append('<title>Dagens mat p&aring; KI - {date}</title>'.format(date = fix_for_html(weekday.capitalize() + ' ' + str(day) + ' ' + str(month))))
    # Google translate support, page must be at correct address for this to work
    lines.append('''<meta name="google-translate-customization" content="85dd414b95fed0f0-aa01444e15709cd9-gfbbe571cd431d573-13"></meta>''')
    lines.append('<link href="http://fonts.googleapis.com/css?family=Lato&amp;subset=latin,latin-ext" rel="stylesheet" type="text/css">')
    lines.append('<link href="styles.css" rel="stylesheet" type="text/css">')
    lines.append('<style type="text/css"></style>')
    lines.append('</head>')
    lines.append('<body>')
    # Google translate support continued
    lines.append('''<div id="google_translate_element"></div><script type="text/javascript">
    function googleTranslateElementInit() {
    new google.translate.TranslateElement({pageLanguage: 'sv', layout: google.translate.TranslateElement.InlineLayout.SIMPLE}, 'google_translate_element');
    }
    </script><script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>''')
    # page formatting
    lines.append('')
    return lines

def parse_61an(filename) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    
    lines = list()
    lines += restaurant_start('Restaurang 61:an', 'Huddinge', 
                              'http://61an.kvartersmenyn.se/', 
                              'https://www.openstreetmap.org/#map=19/59.22071/17.93717')

    started = False
    title_passed = False
    for line in open(filename, encoding='utf8') :
        if 'vecka' in line.lower() and not title_passed and not 'meny' in line.lower():
            note('61an - week found')
            if not str(week) in line :
                error('61an - wrong week')
                break
            title_passed = True
        if weekday in line.lower() and title_passed :
            started = True
            note('61an - day found')
            if tomorrow in line.lower() :
                note('61an - all days on one line')
                days = line.split('<STRONG>')
                if len(days) == 1 :
                    days = line.split('<strong>')
                if len(days) == 1 :
                    error('61an - parsing failed - strong')
                    break
                for d in range(len(days)) :
                    if weekday in days[d].lower() :                        
                        parts = days[d].split('<br />')
                        if len(parts) == 1 :
                            parts = days[d].split('<br>')
                        if len(parts) == 1 :
                            error('61an - parsing failed - br')
                            break
                        note('61an - day found')
                        for i in range(1, len(parts), 1) :
                            if len(fix_for_html(remove_html(parts[i]))) > 0 :
                                lines.append(fix_for_html(remove_html(parts[i]) + '<br/>'))
        if not started :
            continue
        if tomorrow in line.lower() or 'streck2.gif' in line or len(line.strip()) < 25 :
            note('61an - next day reached')
            break
        tmp = line.strip()
        tmp = tmp[tmp.lower().index(weekday) + len(weekday):]
        parts = tmp.split('<BR>')
        for i in range(1, len(parts), 1) :
            lines.append(fix_for_html(remove_html(parts[i]) + '<br/>'))

    lines += restaurant_end()
    return lines

def parse_alfred(filename) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    
    lines = list()
    lines += restaurant_start('Alfreds restaurang', 'Huddinge', 
                              'http://alfredsrestaurang.com/', 
                              'https://www.openstreetmap.org/#map=19/59.21944/17.94074')

    soup = BeautifulSoup(open(filename))

    try :
        menu = soup.find_all('div')[85]

        wdigit = get_weekdigit()
        if wdigit < 5 :
            base = 3 + 7*wdigit
            for i in range(4) :
                lines.append(fix_for_html(remove_html(str(menu.find_all('p')[base + i]))) + '<br/>')

    except :
        error('Alfred crashed')
        
    lines += restaurant_end()

    return lines

def parse_glada(filename) :
    lines = list()
    lines += restaurant_start('Den Glada Restaurangen', 'Solna', 
                              'http://www.dengladarestaurangen.se/', 
                              'http://www.openstreetmap.org/#map=19/59.35123/18.03006')

    week = get_week()
    tomorrow = get_weekday(tomorrow=True)
    today = get_weekday()

    menu_reached = False
    start = False
    for line in open(filename, encoding='utf-8') :
        if 'Vecka' in line and '</h1>' in line :
            if str(week) not in line.lower() :
                error('Glada - wrong week')
            note('Glada - week found')
            menu_reached = True
        if menu_reached and today in line.lower() :
            note('Glada - day found')
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

def parse_haga(filename) :
    lines = list()
    lines += restaurant_start('Haga gatuk&ouml;k', 'Solna', 
                              'http://orenib.se/haga_gk2.pdf', 
                              'https://www.openstreetmap.org/#map=19/59.34931/18.02095')
    lines += restaurant_end()
    return lines
    
def parse_hjulet(filename) :
    day = get_day()
    month = get_month()
    today = get_weekday()

    lines = list()
    lines += restaurant_start('Hjulet', 'Solna', 
                              'http://gastrogate.com/restaurang/restauranghjulet/', 
                              'https://www.openstreetmap.org/#map=19/59.34508/18.02423')

    soup = BeautifulSoup(open(filename))
    # find the weekday index
    DAY_INDEX = None
    i = 0
    try :
        for header in soup.find_all('table')[0].find_all('th') :
            if today in str(header).lower() and str(day) in str(header).lower() and month in str(header).lower() :
                day_index = i
                note('Hjulet - day found')
            i += 1
        if day_index != None :
            txt = remove_html(str(soup.find_all('table')[0].find_all('td')[day_index*3]))
            menu = txt.split('\n')
            for i in range(len(menu)) :
                menu[i] = fix_for_html(menu[i])
                if len(menu[i].strip()) > 0 :
                    lines.append(menu[i] + '<br/>')
            lines.append('<i>Veckans tips:</i> ' + fix_for_html(remove_html(str(soup.find_all('table')[0].find_all('td')[15]))))
        else :
            Error('Hjulet - correct day not found')
    except :
        error('Hjulet crashed')
    lines += restaurant_end()

    return lines

def parse_jons(filename) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    day = get_day()
    month = get_month()
    lines = list()
    lines += restaurant_start('J&ouml;ns Jacob', 'Solna', 
                              'http://gastrogate.com/restaurang/jonsjacob/', 
                              'https://www.openstreetmap.org/#map=19/59.34673/18.02465')

    start = False
    today = '{wday}  {iday} {mon}'.format(wday = weekday, iday = day, mon = month)
    today_alt = '{wday} {iday} {mon}'.format(wday = weekday, iday = day, mon = month)
    current = list()
    for line in open(filename, encoding='utf8') :
        if today in line.lower() or today_alt in line.lower() :
            note('Jöns Jacob - day found')
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

def parse_jorpes(filename) :
    lines = list()
    lines += restaurant_start('Caf&eacute; Erik Jorpes', 'Solna', 
                              'http://restaurang-ns.com/cafe-erik-jorpes/', 
                              'https://www.openstreetmap.org/#map=19/59.34851/18.02721')

    lines += restaurant_end()
    return lines


def parse_karolina(filename) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    day = get_day()
    month = get_month()
    lines = list()
    lines += restaurant_start('Restaurang Karolina', 'Solna', 
                              'http://gastrogate.com/restaurang/ksrestaurangen/', 
                              'https://www.openstreetmap.org/#map=19/59.35224/18.03103')

    start = False
    today = '{wday} {iday} {mon}'.format(wday = weekday, iday = day, mon = month)
    today_alt = '{wday}  {iday} {mon}'.format(wday = weekday, iday = day, mon = month)
    current = list()
    for line in open(filename, encoding='utf8') :
        if today in line.lower() or today_alt in line.lower() :
            note('Karolina - day found')
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

# accuracy not confirmed
def parse_konigs(filename) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    day = get_day()
    month = get_month()
    
    lines = list()
    lines += restaurant_start('Restaurang K&ouml;nigs', 'Solna', 
                              'http://restaurangkonigs.se/', 
                              'https://www.openstreetmap.org/#map=19/59.34959/18.02343')
    start = False
    menu_passed = False
    for line in open(filename, encoding='utf8') :
        if 'VECKA' in line :
            if str(week) not in line :
                error('Königs - wrong week')
                break
        if 'Veckans matsedel:' in line :
            menu_passed = True
            continue

        if menu_passed and (weekday in line.lower() or fix_for_html(weekday) in line.lower()) :
            note('Königs - day found')
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

def parse_matmakarna(filename) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    
    lines = list()
    lines += restaurant_start('Restaurang Matmakarna', 'Huddinge', 
                              'http://www.matmakarna.nu/index.html', 
                              'https://www.openstreetmap.org/#map=19/59.21872/17.94068')
    rad_checker = False
    started = False
    for line in open(filename, encoding='latin1') :
        if 'vecka ' in line.lower() and not started and not 'meny' in line.lower():
            note('Matmakarna - week found')
            if not str(week) in line :
                error('Matmakarna - wrong week')
                break
        if weekday.upper() in line and 'START' in line :
            started = True
            note('Matmakarna - day found')
            continue
        if not started :
            continue
        if weekday.upper() in line and 'SLUT' in line :
            note('Matmakarna - end of day')
            break
#        note(line)
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

def parse_mf(filename) :
    # Funny fact: W3C validator crashes while analysing this page.
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    
    lines = list()
    lines += restaurant_start("MFs Kafe & k&ouml;k", 'Huddinge', 
                              'http://mmcatering.nu/mfs-kafe-kok/', 
                              'https://www.openstreetmap.org/#map=18/59.21813/17.93887')
    if weekday == 'måndag' :
        weekday = 'ndag'

    start = False
    for line in open(filename, encoding = 'latin1') :
        if 'meny vecka' in line.lower() :
            note('MF - week found')
            if 'veckans' in line.lower() :
                continue
            if not str(week) in line :
                error('MF - wrong week')
                break
        if weekday in line.lower() :
            note('MF - day found')
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

def parse_mollan(filename) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    
    lines = list()
    lines += restaurant_start('Mollan', 'Solna', 
                              'http://mollanasiankok.se/', 
                              'https://www.openstreetmap.org/#map=19/59.34836/18.02650')

    soup = BeautifulSoup(open(filename))
    try :
        relevant = soup.find_all('div')[24]
        # check week
        if not str(week) in str(relevant.find_all('div')[0]) :
            error('Mollan - wrong week')

        wdigit = get_weekdigit()
        if wdigit < 5 :
            base = 2 + 7*wdigit
            for i in range(6) :
                lines.append(fix_for_html(remove_html(str(relevant.find_all('p')[base + i]))) + '<br/>')
    except :
        error('Mollan crashed')
            
    lines += restaurant_end()

    return lines

def parse_nanna(filename) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    week = get_week()
    
    lines = list()
    lines += restaurant_start('Restaurang Nanna Svartz', 'Solna', 
                              'http://restaurang-ns.com/restaurang-nanna-svartz/', 
                              'https://www.openstreetmap.org/#map=19/59.34848/18.02807')
    start = False
    for line in open(filename, encoding='utf-8') :
        if 'meny' in line.lower() and 'vecka' in line.lower() :
            if not str(week) in line :
                error('Nanna - wrong week')
                break
            note('Nanna - week found')
        # looking for the lines where the menu is listed in bold text
        if weekday in line.lower() and 'h3' in line.lower() :
            note('Nanna - Day found')
            start = True
            continue
        # alternative formatting
        if weekday in line.lower() and '<strong>' in line.lower() :
            note('Nanna - Day found')
            start = True
            continue
        # end of day
        if start and (tomorrow in line.lower() or '<div class="span6">' in line) :
            note('Nanna - Day ended')
            break
        if start and len(remove_html(line.strip())) > 1 :
            lines.append(fix_for_html(remove_html(line.strip())) + '<br/>')

    lines += restaurant_end()

    return lines

def parse_stories(filename) :
    lines = list()
    lines += restaurant_start('Flemingsberg Stories', 'Huddinge', 
                              'http://www.cafestories.se/', 
                              'https://www.openstreetmap.org/#map=19/59.22050/17.94205')
    lines += restaurant_end()
    return lines

def parse_tango(filename) :
    weekday = get_weekday()
    tomorrow = get_weekday(tomorrow = True)
    day = get_day()
    month = get_month()
    lines = list()
    lines += restaurant_start('Restaurang Tango', 'Huddinge', 
                              'http://gastrogate.com/restaurang/tango/',
                              'https://www.openstreetmap.org/#map=19/59.22042/17.94013')

    start = False
    today = '{wday} {iday} {mon}'.format(wday = weekday, iday = day, mon = month)
    today_alt = '{wday}  {iday} {mon}'.format(wday = weekday, iday = day, mon = month)
#    current = list()
    for line in open(filename, encoding='utf8') :
        if today in line.lower() or today_alt in line.lower() :
            note('Tango - day found')
            start = True
            continue
        if start and (tomorrow in line.lower() or 'gäller hela veckan' in line.lower()) :
            break
        if start :
            tmp = fix_for_html(remove_html(line))
            if len(tmp.strip()) > 4 : # get rid of the line with pricing
#                current.append(tmp.strip())
 #           if '</tr>' in line :
 #               if len(current) > 0 :
                lines.append(tmp.strip() + '<br/>')
 #                   current = list()

    lines += restaurant_end()
    return lines

def parse_subway(filename) :
    wdigit = get_weekdigit()
    # sub of the day
    subotd = {0: 'American Steakhouse Melt', 1: 'Subway Melt', 2: 'Spicy Italian', 3: 'Rostbiff', 4: 'Tonfisk', 5: 'Subway Club', 6: 'Italian B.M.T-', 7: 'American Steakhouse Melt'}
    lines = list()
    lines += restaurant_start('Subway', 'Solna', 
                              'http://subway.se/sv/hem/', 
                              'https://www.openstreetmap.org/#map=19/59.35084/18.02433')
    lines.append('<p> Sub of the day: {0}</p>\n'.format(fix_for_html(subotd[wdigit])))
    lines += restaurant_end()
    return lines


def print_usage(supported) :
    sys.stderr.write('Usage: {} restaurant=filename \n'.format(sys.argv[0]))
    sys.stderr.write('Supported restaurants: {}\n'.format(', '.join(sorted(supported))))

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

if __name__ == '__main__' :
    SUPPORTED = ('jorpes', 'glada', 'haga', 'hjulet', 'jons', 'karolina', 'konigs', 'mollan',
                 'nanna', 'subway', '61an', 'alfred', 'stories','matmakarna', 'mf', 'tango')
    FUNCTIONS = (parse_jorpes, parse_glada, parse_haga, parse_hjulet, parse_jons, parse_karolina, parse_konigs, parse_mollan,
                 parse_nanna, parse_subway, parse_61an, parse_alfred, parse_stories, parse_matmakarna, parse_mf, parse_tango)
    
    if len(sys.argv) < 2 or '-h' in sys.argv :
        print_usage(SUPPORTED)
        sys.exit()
    
    # get filenames
    restaurants = list()
    files = list()
    for param in sys.argv[1:] :
        parts = param.split('=')
        if len(parts) != 2 :
            sys.stderr.write('Error: incorrect parameter: {}\n'.format(param))
            print_usage(SUPPORTED)
            sys.exit()            
        if parts[0] not in SUPPORTED :
            sys.stderr.write('Error: unsupported restaurant: {}\n'.format(parts[0]))
            print_usage(SUPPORTED)
            sys.exit()
        restaurants.append(parts[0].lower())
        files.append(parts[1])

    print('\n'.join(page_start(get_weekday(), str(get_day()), get_month())))
    # print restaurants
    for i in range(len(SUPPORTED)) :
        if SUPPORTED[i] in restaurants :
            print('\n'.join(FUNCTIONS[i](files[restaurants.index(SUPPORTED[i])])))

    print('\n'.join(page_end()))
