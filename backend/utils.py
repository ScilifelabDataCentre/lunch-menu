#!/usr/bin/env python3

# Copyright (c) 2014-2022, Linus Östberg and contributors
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
"""
Main script for choosing what restaurant parsers to use.
"""

import json
import os
import sys

import parser as ps

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
REST_FILENAME = os.path.join(__location__, "restaurants.json")


def read_restaurants(intext: str) -> dict:
    """
    Parse the list of restaurants from the restaurants file.

    Args:
        intext(str): The text loaded from the restaurants file.
    """
    indata = json.loads(intext)
    data = dict()
    for entry in indata["restaurants"]:
        data[entry["identifier"]] = entry
    return data


REST_DATA = read_restaurants(open(REST_FILENAME).read())

MAPPER = {
    "bikupan": ps.parse_bikupan,
    "biomedicum": ps.parse_biomedicum,
    "delta": ps.parse_delta,
    "dufva": ps.parse_dufva,
    "glada": ps.parse_glada,
    "haga": ps.parse_haga,
    "hubben": ps.parse_hubben,
    "jons": ps.parse_jons,
    "jorpes": ps.parse_jorpes,
    "kraemer": ps.parse_kraemer,
    "livet": ps.parse_livet,
    "maethai": ps.parse_maethai,
    "nanna": ps.parse_nanna,
    "rudbeck": ps.parse_rudbeck,
    "street": ps.parse_street,
    "svarta": ps.parse_svarta,
}


def activate_parsers(restaurants, restaurant_data):
    """
    Run the wanted parsers
    """
    output = []
    for restaurant in restaurants:
        data = MAPPER[restaurant](restaurant_data[restaurant])
        output.append(f"""<div class="title"><a href="{data['url']}">{data['title']}</a>""")
        output.append(f"""(<a href="{data['map_url']}">{data['location']}</a>)</div>""")
        if "menu" in data:
            output.append('<div class="menu">')
            output.append("<p>")
            output.append("<br />\n".join(data["menu"]))
            output.append("</p>")
        output.append("</div>")
    return "\n".join(output)


def get_restaurant(name: str) -> dict:
    """
    Request the menu of a restaurant
    """
    if name in MAPPER:
        return MAPPER[name](REST_DATA[name])
    else:
        return {}


def list_restaurants():
    """
    List all supported restaurants.
    """
    return list(REST_DATA.values())
