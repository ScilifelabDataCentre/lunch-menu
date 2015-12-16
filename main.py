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
import sys
import requests

import parser as ps

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
    lines.append('</head>')
    lines.append('<body>')
    # page formatting
    lines.append('')
    return lines

def read_restaurants(filename = 'restaurants.txt') :
    '''Read a text file with the columns:
    #identifier	Name	URL	Menu URL	Open Streetmap'''

    restaurants = list()
    with open(filename) as infile :
        for line in infile :
            if line.lstrip()[0] == '#' :
                continue
            restaurants.append(line.rstrip().split('\t'))
    return restaurants

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

    print('\n'.join(page_start(ps.get_weekday(), str(ps.get_day()), ps.get_month())))
    # print restaurants
    for i in range(len(SUPPORTED)) :
        if SUPPORTED[i] in restaurants :
            print('\n'.join(FUNCTIONS[i](files[restaurants.index(SUPPORTED[i])])))

    print('\n'.join(page_end()))
