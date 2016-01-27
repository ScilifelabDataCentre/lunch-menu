#!/usr/bin/env python3

# Copyright (c) 2014-2016, Linus Östberg
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
import string
import sys

import parser as ps

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
    lines.append('<title>Dagens mat p&aring; KI - {date}</title>'.format(date = ps.fix_for_html(weekday.capitalize() + ' ' + str(day) + ' ' + str(month))))
    lines.append('<link href="styles.css" rel="stylesheet" type="text/css">')
    lines.append('<style type="text/css"></style>')
    lines.append('</head>')
    lines.append('<body>')
    # page formatting
    lines.append('')
    return lines

def print_usage(supported) :
    '''Print description of syntax'''
    sys.stderr.write('Usage: {} restaurant1 [restaurant2] \n'.format(sys.argv[0]))
    sys.stderr.write('Supported restaurants: {}\n'.format(', '.join(sorted(supported))))
    sys.stderr.write('write all to generate all supported restaurants\n')
    sys.stderr.write('-r filepath to use another restaurant list\n')

def read_restaurants(filename) :
    '''Read the list of restaurants'''
    '''Read a tsv file with the columns:
    [0] identifier [1] Name [2] URL [3] Menu URL [4] OSM URL'''

    restaurants = list()
    with open(filename) as infile :
        for line in infile :
            if line.lstrip()[0] == '#' :
                continue
            restaurants.append(line.rstrip().split('\t'))
    return restaurants
    
if __name__ == '__main__' :
    MAPPER = (('jorpes', ps.parse_jorpes), ('glada', ps.parse_glada),
              ('haga', ps.parse_haga), ('hjulet', ps.parse_hjulet),
              ('jons', ps.parse_jons), ('karolina', ps.parse_karolina),
              ('konigs', ps.parse_konigs), ('mollan', ps.parse_mollan),
              ('nanna', ps.parse_nanna), ('svarta', ps.parse_svarta),
              ('subway', ps.parse_subway), ('61an', ps.parse_61an),
              ('alfred', ps.parse_alfred), ('stories', ps.parse_stories),
              ('matmakarna', ps.parse_matmakarna), ('mf', ps.parse_mf),
              ('tango', ps.parse_tango))
    
    if len(sys.argv) < 2 or '-h' in sys.argv :
        print_usage((x[0] for x in MAPPER))
        sys.exit()

    if '-r' in sys.argv :
        RESTAURANTS = sys.argv[sys.argv.index('-r') + 1]
    else :
        RESTAURANTS = 'restaurants.txt'
        
    # get filenames
    restaurant_data = read_restaurants(RESTAURANTS)
    restaurants = list()
    if 'all' in sys.argv[1:] :
        inrest = (x[0] for x in MAPPER)
    elif '-r' in sys.argv :
        inrest = sys.argv[1:sys.argv.index('-r')] + sys.argv[sys.argv.index('-r')+2:]
    else :
        inrest = sys.argv[1:]
    
    for param in inrest :
        if param not in (x[0] for x in MAPPER) :
            if param != '-r' :
                print_usage((x[0] for x in MAPPER))
                sys.exit()
        if param != '-r' :
            restaurants.append(param.lower())

    print('\n'.join(page_start(ps.get_weekday(), str(ps.get_day()), ps.get_month())))
    # print restaurants
    for i in range(len(MAPPER)) :
        if MAPPER[i][0] in restaurants :
            print('\n'.join(MAPPER[i][1](restaurant_data[[x[0] for x in restaurant_data].index([x[0] for x in MAPPER][i])])))

    print('\n'.join(page_end()))
    
