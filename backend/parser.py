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
Parsers of the menu pages for the restaurants at Karolinska Institutet
"""

import datetime
from datetime import date
import re
import sys

import requests
from bs4 import BeautifulSoup
from collections import defaultdict


def restaurant(func):
    """
    Decorator to use for restaurants.
    """

    def helper(res_data):
        data = {
            "title": res_data["name"],
            "location": res_data["region"],
            "url": res_data["homepage"],
            "map_url": res_data["osm"],
        }
        try:
            data.update(func(res_data))
        except Exception as err:
            sys.stderr.write(f"E in {func.__name__}: {err}\n")
            data.update({"menu": []})
            pass
        return data

    helper.__name__ = func.__name__
    helper.__doc__ = func.__doc__

    return helper


def get_parser(url: str) -> BeautifulSoup:
    """
    Request page and create Beautifulsoup object
    """
    page_req = requests.get(url)
    if page_req.status_code != 200:
        raise IOError("Bad HTTP responce code")

    return BeautifulSoup(page_req.text, "html.parser")


def fix_bad_symbols(text):
    """
    HTML formatting of characters
    """
    text = text.replace("Ã¨", "è")
    text = text.replace("Ã¤", "ä")
    text = text.replace("Ã", "Ä")
    text = text.replace("Ã", "Ä")
    text = text.replace("Ã¶", "ö")
    text = text.replace("Ã©", "é")
    text = text.replace("Ã¥", "å")
    text = text.replace("Ã", "Å")

    text = text.strip()

    return text


### date management start ###
def get_day():
    """
    Today as digit
    """
    return date.today().day


def get_monthdigit():
    """
    Month as digit
    """
    return date.today().month


def get_month():
    """
    Month name
    """
    months = {
        1: "januari",
        2: "februari",
        3: "mars",
        4: "april",
        5: "maj",
        6: "juni",
        7: "juli",
        8: "augusti",
        9: "september",
        10: "oktober",
        11: "november",
        12: "december",
    }

    return months[get_monthdigit()]


def get_week():
    """
    Week number
    """
    return date.today().isocalendar()[1]


def get_weekday(lang="sv", tomorrow=False):
    """
    Day name in swedish(sv) or english (en)
    """
    wdigit = get_weekdigit()
    if tomorrow:
        wdigit += 1
    if lang == "sv":
        weekdays = {
            0: "måndag",
            1: "tisdag",
            2: "onsdag",
            3: "torsdag",
            4: "fredag",
            5: "lördag",
            6: "söndag",
            7: "måndag",
        }
    if lang == "en":
        weekdays = {
            0: "monday",
            1: "tuesday",
            2: "wednesday",
            3: "thursday",
            4: "friday",
            5: "saturday",
            6: "sunday",
            7: "monday",
        }
    return weekdays[wdigit]


def get_weekdigit():
    """
    Get digit for week (monday = 0)
    """
    return date.today().weekday()


def get_year():
    """
    Year as number
    """
    return date.today().year


### date management end ###

### parsers start ###
@restaurant
def parse_bikupan(res_data: dict) -> dict:
    """
    Parse the menu of Restaurang Bikupan
    """

    def fmt_paragraph(p):
        return p.get_text().strip().replace("\n", " ")

    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])
    # check week number
    target = soup.find("div", {"id": "current"})
    if str(get_week()) not in target.find("h2").text:
        return data
    raw_menu = target.find("div", {"class": "menu-item " + get_weekday(lang="en")})
    for entry in raw_menu.find_all("p"):
        # skip rows with english
        if "class" in entry.attrs and "eng-meny" in entry.attrs["class"]:
            continue
        data["menu"].append(entry.text.strip())

    return data


@restaurant
def parse_biomedicum(res_data):
    """
    No homepage for Café Biomedicum.
    """
    return {"menu": []}


@restaurant
def parse_delta(res_data):
    """
    No homepage for Café Delta.
    """
    return {"menu": []}


@restaurant
def parse_dufva(res_data):
    """
    Parse the menu of Sven Dufva
    """
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    relevant = soup.find("div", {"id": "post"})
    menu_data = relevant.get_text().split("\n")
    dag = get_weekday()
    started = False
    for line in menu_data:
        if not line:
            continue
        if line.lower() == f"- {dag} -":
            started = True
            continue
        if started:
            if line[0] != "-":
                data["menu"].append(line.strip())
            else:
                break
    return data


@restaurant
def parse_glada(res_data):
    """
    Parse the menu of Glada restaurangen
    """
    data = {"menu": []}
    # No way I'll parse this one. If anyone actually wants to, I'd be happy to accept a patch.
    return data


@restaurant
def parse_haga(res_data):
    """
    Empty parser for Haga Gatukök.
    """
    return {"menu": []}


@restaurant
def parse_hubben(res_data):
    """
    Parse the menu of Restaurang Hubben
    """
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    days = soup.find_all("div", {"class": "day"})
    current = days[get_weekdigit()]
    dishes = current.find_all("div", {"class": "element description col-md-4 col-print-5"})
    for dish in dishes:
        data["menu"].append(dish.get_text().strip().replace("\n", " "))

    return data


@restaurant
def parse_jons(res_data):
    """
    Parse the menu of Jöns Jacob
    """
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    days = soup.find("table", {"class": "table lunch_menu animation"})
    day = days.find("tbody", {"class": "lunch-day-content"})
    dishes = day.find_all("td", {"class": "td_title"})
    data["menu"] += [dish.text.strip() for dish in dishes if dish.text.strip()]

    return data


@restaurant
def parse_jorpes(res_data):
    """
    Parse the menu of Resturang Jorpes
    """
    return {"menu": []}


@restaurant
def parse_kraemer(res_data):
    """
    No menu for Hotel von Kraemer.
    """
    return {"menu": []}


@restaurant
def parse_livet(res_data):
    """
    Parse the menu of Livet
    """
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])
    content = soup.find("div", {"class": "content"})
    weekday = get_weekday()
    weekday = f"[{weekday[0]}{weekday[0].upper()}]{weekday[1:]}"
    month = get_month()
    month = f"[{month[0]}{month[0].upper()}]{month[1:]}"
    re_today = f"{weekday} {get_day()} {month}"

    started = False
    for tag in content.find_all(("strong", "ul")):
        if tag.find(text=re.compile(re_today)):
            started = True
            continue
        if started:
            if tag.name == "ul":
                data["menu"] = [entry.text for entry in tag.find_all("li") if entry.text.strip()]
            break
    return data


@restaurant
def parse_maethai(res_data):
    """
    Parse the menu of Mai Thai Express
    """
    return {"menu": []}


@restaurant
def parse_nanna(res_data):
    """
    Parse the menu of Nanna Svartz.
    """
    return {"menu": []}


@restaurant
def parse_rudbeck(res_data):
    """
    Parse the menu of Bistro Rudbeck
    """
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    menu_part = soup.find("div", {"class": "menu-item " + get_weekday(lang="en")})

    for entry in menu_part.find_all("p"):
        if "class" not in entry.attrs:
            text = entry.text.strip()
            if text[0] == "-":
                text = text[1:].lstrip()
            data["menu"].append(text)
    return data


@restaurant
def parse_street(res_data):
    """
    Parse the menu of STHLM Street Food.

    Image-based menu, i.e. no parser.
    """
    return {"menu": []}


@restaurant
def parse_svarta(res_data):
    """
    Parse the menu of Svarta Räfven
    """
    return {"menu": []}


@restaurant
def parse_tallrik(res_data):
    """
    Parse the menu of Tallriket
    """
    data = {"menu": []}
    soup = get_parser(res_data["menuUrl"])

    days = soup.find_all("div", {"class": "container-fluid no-print"})
    day = days[get_weekdigit()]
    dishes = day.find_all("span")[3:]
    for dish in [x for x in dishes if x.get_text().strip() != ""]:
        data["menu"].append(dish.get_text().strip())

    return data
