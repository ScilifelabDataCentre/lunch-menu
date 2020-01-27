#!/usr/bin/env python3

# Copyright (c) 2014-2020, Linus Östberg
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

import click
import os
import sys
import requests
import requests_cache
import json

import parser as ps

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
REST_FILENAME = os.path.join(__location__, 'restaurants.txt')

def read_restaurants(intext):
    '''
    Read the list of restaurants
    Read a tsv file with the columns:
    [0] campus [1] identifier [2] Name [3] URL [4] Menu URL [5] OSM URL
    '''
    restaurants = {}
    col_names = ('campus', 'identifier', 'name', 'url', 'menu_url', 'osm')
    for line in intext.split('\n'):
        if not line or line[0] == '#':
            continue
        cols = line.rstrip().split('\t')
        values = dict(zip(col_names, cols))
        restaurants[values['identifier']] = values
    return restaurants


REST_DATA = read_restaurants(open(REST_FILENAME).read())

# works as ordered dict as well, but must be _ordered_
MAPPER = {'jorpes': ps.parse_jorpes, 'glada': ps.parse_glada,
          'haga': ps.parse_haga, 'hjulet': ps.parse_hjulet,
          'jons': ps.parse_jons, 'livet': ps.parse_livet,
          'nanna': ps.parse_nanna, 'svarta': ps.parse_svarta,
          'bikupan': ps.parse_bikupan, 'dufva': ps.parse_dufva,
          'hubben': ps.parse_hubben, 'rudbeck': ps.parse_rudbeck,
          'tallrik': ps.parse_tallrik}

KI = ('jorpes', 'glada', 'haga', 'hjulet', 'jons',
      'livet', 'nanna', 'svarta')

UU = ('bikupan', 'dufva', 'hubben', 'rudbeck', 'tallrik')

ALL = KI + UU


def build_output(data, fmt):
    output = list()
    if fmt == 'html':
        output.append(f'''<div class="title"><a href="{data['url']}">{data['title']}</a>''')
        output.append(f'''(<a href="{data['map_url']}">{data['location']}</a>)</div>''')
        output.append('<div class="menu">')
        output.append('<p>')
        output.append('<br />\n'.join(data['menu']))
        output.append('</p>')
        output.append('</div>')
    elif fmt == 'markdown':
        # Simple markdown like format, for example slack or a terminal:
        output.append(f'*{data["title"]}*')
        for menu in data['menu']:
            output.append('> {}'.format(menu))
    else:
        raise NotImplementedError(fmt)
    return '\n'.join(output)


def activate_parsers(restaurants, restaurant_data, fmt='html'):
    '''
    Run the wanted parsers
    '''
    output = []
    for restaurant in restaurants:
        try:
            data = MAPPER[restaurant](restaurant_data[restaurant])
        except Exception as err:
            sys.stderr.write(f'E in {restaurant}: {err}\n')
        output.append(build_output(data, fmt))
    return output


def get_restaurant(name: str) -> dict:
    '''
    Request the menu of a restaurant
    '''
    if name in MAPPER:
        return MAPPER[name](REST_DATA[name])
    else:
        return {}


def list_restaurants():
    '''
    List all supported restaurants.
    '''
    return list(REST_DATA.values())


def page_end():
    '''
    Print the closure of tags etc
    '''
    lines = list()
    lines.append('<div class="endnote">Code available at ' +
                 '<a href="https://github.com/talavis/lunch-menu">' +
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
    date = weekday.capitalize() + ' ' + str(day) + ' ' + str(month)
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
        if param not in ALL:
            raise ValueError('{} not a valid restaurant'.format(param))
        restaurants.append(param.lower())
    return restaurants

def gen_menu(restaurants, restaurant_data, fmt):
    data = activate_parsers(restaurants, restaurant_data, fmt)

    output = list()
    if fmt == 'html':
        output.extend(page_start(ps.get_weekday(), str(ps.get_day()), ps.get_month()))
        output.extend(data)
        output.extend(page_end())
    else:
        output.extend(data)
    return '\n'.join(output)



def gen_ki_menu():
    '''
    Generate a menu for restaurants at KI
    '''
    return gen_menu(KI, REST_DATA)


def gen_uu_menu():
    '''
    Generate a menu for restaurants at UU
    '''
    return gen_menu(UU, REST_DATA)


SLACK_HELP = '''Send to a particular slack channel instead of writing to stdout.
  You must also set the environment variable LUNCH_MENU_SLACK_WEBHOOK.



@click.command()
@click.option('--cache/--no-cache', default=False, help='Cache web request for debugging')
@click.option('--slack-channel', help='Sends the data to the specified channel')
@click.option('--slack-user', help='Slack user that posts the message', default='lunchbot')
@click.option('--slack-emoji', help='Emoji for the post', default=':croissant:')
@click.option('--fmt', default='html', type=click.Choice(('html', 'markdown')), help='The format of the output')
@click.argument('restaurants', nargs=-1, type=click.Choice(('all', 'ki', 'uu') + ALL))
def main(restaurants, cache, slack_channel, slack_user, slack_emoji, fmt):
    '''Generates a report for the selected restaurant(s)'''

    if cache:
        # Caches all web requests in the file demo_cache. Just for testing.
        requests_cache.install_cache('.devcache')

    REST_NAMES_IN = tuple()
    if 'all' in restaurants:
        REST_NAMES_IN += ALL
    elif 'ki' in restaurants:
        REST_NAMES_IN += KI
    elif 'uu' in restaurants:
        REST_NAMES_IN += UU
    else:
        # NOTE: There was some undocumented -r flag here
        REST_NAMES_IN = restaurants

    try:
        REST_NAMES = parse_restaurant_names(REST_NAMES_IN)
    except ValueError as err:
        sys.stderr.write('E: {}\n'.format(err))
        print_usage((x for x in MAPPER))
        sys.exit(1)

    if slack_channel:
        fmt = 'markdown'

    menu = gen_menu(REST_NAMES, REST_DATA, fmt)

    if slack_channel:
        if slack_channel.startswith('#'):
            slack_channel = '#' + slack_channel
        URL = os.environ['LUNCH_MENU_SLACK_WEBHOOK']
        post_payload = {'channel': slack_channel,
                        'username': slack_user,
                        'icon_emoji': slack_emoji,
                        'text': menu}
        post_response = requests.post(URL, data=json.dumps(post_payload))
        print('Response[{}]: {}'.format(post_response.status_code, post_response.text))
    else:
        print(menu)



if __name__ == '__main__':
    main()

