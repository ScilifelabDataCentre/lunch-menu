kimenu
======

Scripts useful for parsing the menus of the restaurants at Karolinska Institutet and generating a simple html page.

Usage:
python3 main.py <restaurant_name> > index.html

Supported restaurants are listed in restaurants.txt, accepted parameters are the names in column 1 or all to generate the menu for all restaurants. The terms are also listed when you run main.py without any arguments.

Required libraries:
beautiful soup 4
