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
    text = text.strip()
    return text

def note(text) :
    if DEBUG :
        sys.stderr.write('NOTE: ' + text + '\n')

        
def parse_hjulet(filename, today, tomorrow, day, month) :
    lines = list()
    lines += restaurant_start('Hjulet', 'Solna', 
                              'http://gastrogate.com/restaurang/restauranghjulet/', 
                              'https://www.openstreetmap.org/#map=19/59.34508/18.02423')

    soup = BeautifulSoup(open(filename))
    # find the weekday index
    DAY_INDEX = None
    i = 0

    for header in soup.find_all('table')[1].find_all('th') :
        if WEEKDAY in str(header).lower() :
            DAY_INDEX = i
            break
        i += 1

    txt = remove_html(str(soup.find_all('table')[1].find_all('td')[DAY_INDEX*3]))
    txt = txt.replace('\n', '<br>\n')
    lines.append(fix_for_html(txt))

    lines += restaurant_end()
    return lines

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
    SUPPORTED = ('mollan', 'jons', 'hjulet', 'konigs', 'glada', 'nanna', 'subway', 'karolina',
                 'tango', 'mf', 'alfred', 'matmakarna', 'jorpes', 'tango', '61an', 'haga', 
                 'stories')
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
        
    # stuff for conversions, always use versals when comparing to these
    MONTHS = {1: 'januari', 2: 'februari', 3: 'mars', 4: 'april', 5: 'maj', 6: 'juni',
                  7: 'juli', 8: 'augusti', 9: 'september', 10: 'oktober', 11: 'november', 12: 'december'}

    # måndag = ndag is only because of the f-cking jöns jacob page behaving in a f-cked up way.
    WEEKDAYS = {0: 'måndag', 1: 'tisdag', 2: 'onsdag', 3: 'torsdag', 
                4: 'fredag', 5: 'lördag', 6: 'söndag', 7: 'måndag'}
    WEEKDAYS_ENG = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 
                    4: 'friday', 5: 'saturday', 6: 'sunday', 7: 'monday'}

    # current date
    DAY = date.today().day
    MONTH = date.today().month
    WEEK = date.today().isocalendar()[1]
    WDIGIT = date.today().weekday()
    WEEKDAY = WEEKDAYS[WDIGIT]
    WEEKDAY_ENG = WEEKDAYS_ENG[WDIGIT]
    TOMORROW = WEEKDAYS[WDIGIT+1]

    print('\n'.join(page_start(WEEKDAY, str(DAY), MONTHS[MONTH])))
    # solna
    if 'jorpes' in restaurants :
        print('\n'.join(parse_jorpes()))

    if 'glada' in restaurants :
        print('\n'.join(parse_glada(files[restaurants.index('glada')], WEEKDAY, TOMORROW, WEEK, WEEKDAY_ENG)))

    if 'jons' in restaurants :
        print('\n'.join(parse_jons(files[restaurants.index('jons')], WEEKDAY, TOMORROW, DAY, MONTHS[MONTH])))

    if 'haga' in restaurants :
        print('\n'.join(parse_haga()))

    if 'hjulet' in restaurants :
        print('\n'.join(parse_hjulet(files[restaurants.index('hjulet')], WEEKDAY, TOMORROW, DAY, MONTHS[MONTH])))

    if 'karolina' in restaurants :
        print('\n'.join(parse_karolina(files[restaurants.index('karolina')], WEEKDAY, TOMORROW, DAY, MONTHS[MONTH])))

    if 'konigs' in restaurants :
        print('\n'.join(parse_konigs(files[restaurants.index('konigs')], WEEKDAY, TOMORROW, WEEK, DAY, MONTH)))

    if 'mollan' in restaurants :
        print('\n'.join(parse_mollan(files[restaurants.index('mollan')], WEEKDAY, TOMORROW, WEEK)))

    if 'nanna' in restaurants :
        print('\n'.join(parse_nanna(files[restaurants.index('nanna')], WEEKDAY, TOMORROW, WEEK)))

    if 'subway' in restaurants :
        print('\n'.join(parse_subway(WDIGIT)))

    # huddinge
    if '61an' in restaurants :
        print('\n'.join(parse_61an(files[restaurants.index('61an')], WEEKDAY, TOMORROW, WEEK)))

    if 'alfred' in restaurants :
        print('\n'.join(parse_alfred(files[restaurants.index('alfred')], WEEKDAY, TOMORROW, WEEK)))

    if 'mf' in restaurants :
        print('\n'.join(parse_mf(files[restaurants.index('mf')], WEEKDAY, TOMORROW, WEEK)))

    if 'stories' in restaurants :
        print('\n'.join(parse_stories()))

    if 'matmakarna' in restaurants :
        print('\n'.join(parse_matmakarna(files[restaurants.index('matmakarna')], WEEKDAY, TOMORROW, WEEK)))
        
    if 'tango' in restaurants :
        print('\n'.join(parse_tango(files[restaurants.index('tango')], WEEKDAY, TOMORROW, DAY, MONTHS[MONTH])))



    print('\n'.join(page_end()))
