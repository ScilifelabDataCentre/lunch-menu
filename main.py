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
import requests

import parser as ps

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

# page end, ie closing tags etc
def page_end() :
    lines = list()
    lines.append('<div class="endnote">Code available at <a href="https://github.com/talavis/kimenu">Github</a>. Patches are very welcome.</div>')
    lines.append('</body>')
    lines.append('</html>')
    return lines

# page start, including google translate support
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



def print_usage(supported) :
    sys.stderr.write('Usage: {} restaurant=filename \n'.format(sys.argv[0]))
    sys.stderr.write('Supported restaurants: {}\n'.format(', '.join(sorted(supported))))

if __name__ == '__main__' :
    SUPPORTED = ('jorpes', 'glada', 'haga', 'hjulet', 'jons',
                 'karolina', 'konigs', 'mollan', 'nanna', 'svarta',
                 'subway', '61an', 'alfred', 'stories','matmakarna',
                 'mf', 'tango')
    FUNCTIONS = (ps.parse_jorpes, ps.parse_glada, ps.parse_haga, ps.parse_hjulet, ps.parse_jons,
                 ps.parse_karolina, ps.parse_konigs, ps.parse_mollan, ps.parse_nanna, ps.parse_svarta,
                 ps.parse_subway, ps.parse_61an, ps.parse_alfred, ps.parse_stories, ps.parse_matmakarna,
                 ps.parse_mf, ps.parse_tango)
    
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