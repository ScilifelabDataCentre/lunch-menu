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
Main script for choosing what restaurant parsers to use
'''

import os
import sys

import parser as ps

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
REST_FILENAME = os.path.join(__location__, 'restaurants.txt')

# works as ordered dict as well, but must be _ordered_
MAPPER = (('jorpes', ps.parse_jorpes), ('glada', ps.parse_glada),
          ('haga', ps.parse_haga), ('hjulet', ps.parse_hjulet),
          ('jons', ps.parse_jons), ('livet', ps.parse_livet),
          ('mollan', ps.parse_mollan), ('nanna', ps.parse_nanna),
          ('svarta', ps.parse_svarta), ('subway', ps.parse_subway),
          ('bikupan', ps.parse_bikupan), ('dufva', ps.parse_dufva),
          ('hubben', ps.parse_hubben), ('rudbeck', ps.parse_rudbeck))


def activate_parsers(restaurants, restaurant_data):
    '''
    Run the wanted parsers
    '''
    output = []
    for i in range(len(MAPPER)):
        if MAPPER[i][0] in restaurants:
            try:
                to_use = restaurant_data[[x[0] for x in restaurant_data].index(
                    [x[0] for x in MAPPER][i])]
                output.append('\n'.join(MAPPER[i][1](to_use)))
            except Exception as err:
                sys.stderr.write('E in {}: {}\n'.format(MAPPER[i][0], err))
    return '\n'.join(output)


def page_end():
    '''
    Print the closure of tags etc
    '''
    lines = list()
    lines.append('<div class="endnote">Code available at ' +
                 '<a href="https://github.com/talavis/kimenu">' +
                 'Github</a>. Patches are very welcome.</div>')
    lines.append('</body>')
    lines.append('</html>')
    return lines


def page_start(weekday, day, month):
    '''
    Print the initialisation of the page
    '''
    lines = list()
    lines.append('<html>')
    lines.append('<head>')
    date = ps.fix_for_html(weekday.capitalize() + ' ' + str(day) + ' ' + str(month))
    lines.append('<title>Dagens mat - {}</title>'.format(date))
    lines.append('<link href="styles.css" rel="stylesheet" type="text/css">')
    lines.append('<style type="text/css"></style>')
    lines.append('</head>')
    lines.append('<body>')
    # page formatting
    lines.append('')
    return lines


def parse_restaurant_names(rest_names):
    '''
    Decide what restaurants to generate menus for
    '''
    restaurants = list()
    for param in rest_names:
        if param not in (x[0] for x in MAPPER):
            raise ValueError('{} not a valid restaurant'.format(param))
        restaurants.append(param.lower())
    return restaurants


def print_usage(supported):
    '''
    Print description of syntax
    '''
    sys.stderr.write('Usage: {} restaurant1 [restaurant2] \n'.format(sys.argv[0]))
    sys.stderr.write('Supported restaurants: {}\n'.format(', '.join(sorted(supported))))
    sys.stderr.write('write all to generate all supported restaurants\n')


def read_restaurants(intext):
    '''
    Read the list of restaurants
    Read a tsv file with the columns:
    [0] identifier [1] Name [2] URL [3] Menu URL [4] OSM URL
    '''
    restaurants = list()
    for line in intext.split('\n'):
        if not line or line[0] == '#':
            continue
        restaurants.append(line.rstrip().split('\t'))
    return restaurants


def gen_ki_menu():
    '''
    Generate a menu for restaurants at KI
    '''
    restaurant_data = read_restaurants(open(REST_FILENAME).read())
    rest_names = [x[0] for x in MAPPER[:10]]

    output = ''
    output += '\n'.join(page_start(ps.get_weekday(), str(ps.get_day()), ps.get_month()))
    output += activate_parsers(rest_names, restaurant_data)
    output += '\n'.join(page_end())
    return output


def gen_uu_menu():
    '''
    Generate a menu for restaurants at UU
    '''
    restaurant_data = read_restaurants(open(REST_FILENAME).read())
    rest_names = [x[0] for x in MAPPER[10:]]

    output = ''
    output += '\n'.join(page_start(ps.get_weekday(), str(ps.get_day()), ps.get_month()))
    output += activate_parsers(rest_names, restaurant_data)
    output += '\n'.join(page_end())

    sys.stderr.write(output)
    return output


if __name__ == '__main__':
    if len(sys.argv) < 2 or '-h' in sys.argv:
        print_usage((x[0] for x in MAPPER))
        sys.exit()

    RESTAURANT_DATA = read_restaurants(open(REST_FILENAME).read())
    if 'all' in sys.argv[1:]:
        REST_NAMES_IN = (x[0] for x in MAPPER)
    else:
        REST_NAMES_IN = [param for param in sys.argv[1:] if param != '-r']

    try:
        REST_NAMES = parse_restaurant_names(REST_NAMES_IN)
    except ValueError as err:
        sys.stderr.write('E: {}'.format(err))
        print_usage((x[0] for x in MAPPER))
        sys.exit(1)

    # print the menus
    print('\n'.join(page_start(ps.get_weekday(), str(ps.get_day()), ps.get_month())))
    print(activate_parsers(REST_NAMES, RESTAURANT_DATA))
    print('\n'.join(page_end()))
