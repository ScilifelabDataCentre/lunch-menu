#!/usr/bin/env python3

import sys
from datetime import date
import codecs
import string

# global variable to handle displaying of debug messages
DEBUG = True

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
    text = text.strip()
    return text

def error(text) :
    if DEBUG :
        sys.stderr.write('ERROR: ' + text + '\n')

def note(text) :
    if DEBUG :
        sys.stderr.write('NOTE: ' + text + '\n')

def page_end() :
    lines = list()
    lines.append('<small><p>Code available at <a href="https://github.com/talavis/kimenu">Github</a>. Patches are very welcome.</p></small>')
    lines.append('</body>')
    lines.append('</html>')
    return lines

def page_start(weekday, day, month) :
    lines = list()
    lines.append('<html>')
    lines.append('<head>')
    lines.append('<title>Dagens mat p&aring; KI - {date}</title>'.format(date = fix_for_html(weekday.capitalize() + ' ' + str(day) + ' ' + str(month))))
    lines.append('''<meta name="google-translate-customization" content="85dd414b95fed0f0-aa01444e15709cd9-gfbbe571cd431d573-13"></meta>''')
    lines.append('</head>')
    lines.append('<body>')
    lines.append('''<div id="google_translate_element"></div><script type="text/javascript">
    function googleTranslateElementInit() {
    new google.translate.TranslateElement({pageLanguage: 'sv', layout: google.translate.TranslateElement.InlineLayout.SIMPLE}, 'google_translate_element');
    }
    </script><script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>''')
    lines.append('</p>')
    return lines

def parse_61an(filename, weekday, tomorrow, week) :
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
                for d in range(len(days)) :
                    if weekday in days[d].lower() :                        
                        parts = days[d].split('<BR>')
                        note('61an - all days on one line - day found')
                        for i in range(1, len(parts), 1) :
                            if len(fix_for_html(remove_html(parts[i]))) > 0 :
                                lines.append(fix_for_html(remove_html(parts[i]) + '<br/>'))
        if not started :
            continue
        if tomorrow in line.lower() or 'streck2.gif' in line :
            note('61an - next day reached')
            break
        tmp = line.strip()
        tmp = tmp[tmp.lower().index(weekday) + len(weekday):]
        parts = tmp.split('<BR>')
        for i in range(2, len(parts), 2) :
            lines.append(fix_for_html(remove_html(parts[i]) + '<br/>'))

    lines += restaurant_end()
    return lines

def parse_alfred(filename, weekday, tomorrow, week) :
    lines = list()
    lines += restaurant_start('Alfreds restaurang', 'Huddinge', 
                              'http://alfredsrestaurang.com/', 
                              'https://www.openstreetmap.org/#map=19/59.21944/17.94074')

    started = False
    for line in open(filename, encoding='latin1') :
        if 'vecka' in line.lower() and not started :
            if not str(week) in line :
                break
        if fix_for_html(weekday) in line.lower() :
            note('Alfred - day found')
            started = True
            continue
        if not started :
            continue
        if fix_for_html(tomorrow) in line.lower() or 'I samtliga r&auml;tter' in line:
            break
        tmp = remove_html(line.strip())
        if len(tmp) > 0 :
            lines.append(tmp + '<br/>')

    lines += restaurant_end()
    return lines

def parse_glada(filename, weekday, tomorrow, week, weekday_eng) :
    lines = list()
    lines += restaurant_start('Den Glada Restaurangen', 'Solna', 
                              'http://www.dengladarestaurangen.se/', 
                              'http://www.openstreetmap.org/#map=19/59.35123/18.03006')

#    for line in open(filename, encoding='utf-8') :
        # looking for the lines where the menu is listed in bold text
#        if 'Meny v.' in line :
#            if not str(week) in line :
#                error('Glada - wrong week')
#                break
#            note('Glada - week found')
#        if weekday in line.lower() :
            # start after tags
#            spos = line.lower().index(weekday) + len(weekday)
            # stop at end of swedish
#            lines.append(fix_for_html(remove_html(line[spos:line.lower().index(weekday_eng)])))
#            break
        
    lines += restaurant_end()

    return lines

def parse_haga() :
    lines = list()
    lines += restaurant_start('Haga gatuk&ouml;k', 'Solna', 
                              'http://orenib.se/haga_gk2.pdf', 
                              'https://www.openstreetmap.org/#map=19/59.34931/18.02095')
    lines += restaurant_end()
    return lines
    

def parse_hjulet(filename, weekday, tomorrow, week) :
    lines = list()
    lines += restaurant_start('Hjulet', 'Solna', 
                              'http://web.comhem.se/hjulet/index.html', 
                              'https://www.openstreetmap.org/#map=19/59.34508/18.02423')

    start = False
    tips = False
    menu_passed = False
    for line in open(filename, encoding = 'latin1') :
        if not start and 'MENY VECKA' in line :
            if not 'MENY VECKA ' + str(week) in line :
                break
            else :
                menu_passed = True
        if weekday in line.lower() and menu_passed :
            start = True
            continue
        if tips and weekday not in ('lördag', 'söndag') :
            if len(fix_for_html(remove_html(line)).strip()) == 0 :
                continue
            else : 
                lines.append('<i>Veckans tips:</i> ' + fix_for_html(remove_html(line)).strip() + '<br/>')
            break
        if 'VECKANS TIPS' in line :
            note('Hjulet - tips found')
            tips = True
            continue
        if not start :
            continue
        if tomorrow in line.lower() :
            start = False
            continue
        if len(fix_for_html(remove_html(line)).strip()) == 0 :
            continue
        else : 
            tmp = fix_for_html(remove_html(line)).strip()
            if 'align="right"' in line :
                continue
            lines.append(tmp + '<br/>')

    lines += restaurant_end()

    return lines

def parse_jons(filename, weekday, tomorrow, day, month) :
    lines = list()
    lines += restaurant_start('J&ouml;ns Jacob', 'Solna', 
                              'http://gastrogate.com/restaurang/jonsjacob/', 
                              'https://www.openstreetmap.org/#map=19/59.34673/18.02465')

    start = False
    today = '{wday}  {iday} {mon}'.format(wday = weekday, iday = day, mon = month)
    today_alt = '{wday}  {iday} {mon}'.format(wday = weekday, iday = day, mon = month)
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

def parse_jorpes() :
    lines = list()
    lines += restaurant_start('Caf&eacute; Erik Jorpes', 'Solna', 
                              'http://restaurang-ns.com/cafe-erik-jorpes/', 
                              'https://www.openstreetmap.org/#map=19/59.34851/18.02721')

    lines += restaurant_end()
    return lines


def parse_karolina(filename, weekday, tomorrow, day, month) :
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
def parse_konigs(filename, weekday, tomorrow, week, day, month) :
    lines = list()
    lines += restaurant_start('Restaurang K&ouml;nigs', 'Solna', 
                              'http://restaurangkonigs.se/', 
                              'https://www.openstreetmap.org/#map=19/59.34959/18.02343')
    start = False
    menu_passed = False
    for line in open(filename, encoding='utf8') :
        if 'Veckans matsedel:' in line :
            menu_passed = True
#            if not start :
#                if not ('v ' + str(week) in line or  'v ' + str(week) in line) :
#                    note('Königs - correct week')
#                    break
        if menu_passed and weekday in line.lower() :
            note('Königs - correct day')
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

def parse_matmakarna(filename, weekday, tomorrow, week) :
    lines = list()
    lines += restaurant_start('Restaurang Matmakarna', 'Huddinge', 
                              'http://www.matmakarna.nu/index.html', 
                              'https://www.openstreetmap.org/#map=19/59.21872/17.94068')

    started = False
    title_passed = False
    for line in open(filename, encoding='latin1') :
        if 'vecka ' in line.lower() and not started and not 'meny' in line.lower():
            note('Matmakarna - week found')
            if not str(week) in line :
                error('Matmakarna - wrong week')
                break
            title_passed = True
        if fix_for_html(weekday) in line.lower() and title_passed :
            started = True
            note('Matmakarna - day found')
        if not started :
            continue
        if tomorrow in line.lower() or 'streck2.gif' in line :
            note('Matmakarna - next day reached')
            break
        tmp = line.strip()
        tmp = tmp[tmp.lower().index(weekday) + len(weekday):]
        parts = tmp.split('<BR>')
        for i in range(2, len(parts), 2) :
            lines.append(fix_for_html(remove_html(parts[i]) + '<br/>'))

    lines += restaurant_end()
    return lines

def parse_mf(filename, weekday, tomorrow, week) :
    # Funny fact: W3C validator crashes while analysing this page.
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

def parse_mollan(filename, weekday, tomorrow, week) :
    lines = list()
    lines += restaurant_start('Mollan', 'Solna', 
                              'http://mollanasiankok.se/', 
                              'https://www.openstreetmap.org/#map=19/59.34836/18.02650')
    start = False
    for line in open(filename, encoding='latin1') :
        if not start and 'Lunch Meny V.' in line and not str(week) in line :
            break
        if weekday in line.lower() :
            start = True
            continue
        if not start :
            continue
        if tomorrow in line.lower() :
            break
        if '=Gluten' in line :
            break
        tmp = fix_for_html(remove_html(line))
        try :
            if tmp[0] in string.ascii_uppercase and tmp[1] == '.' :
                tmp = tmp[2:]
        except :
            pass
        tmp = tmp.replace('<br/>', ' ')
        if len(tmp) > 0 :
            lines.append(tmp + '<br/>')

    lines += restaurant_end()

    return lines

def parse_nanna(filename, weekday, tomorrow, week) :
    lines = list()
    lines += restaurant_start('Restaurang Nanna Svartz', 'Solna', 
                              'http://restaurang-ns.com/restaurang-nanna-svartz/', 
                              'https://www.openstreetmap.org/#map=19/59.34848/18.02807')
    start = False
    for line in open(filename, encoding='utf-8') :
        if "Meny vecka" in line :
            if not str(week) in line :
                error('Nanna - wrong week')
                break
            note('Nanna - week found')
        # looking for the lines where the menu is listed in bold text
        if weekday in line.lower() and '<h3>' in line.lower() :
            note('Nanna - Day found')
            start = True
            continue
        if start and (tomorrow in line.lower() or '<div class="span6">' in line) :
            note('Nanna - Day ended')
            break
        if start and len(remove_html(line.strip())) > 1 :
            lines.append(fix_for_html(remove_html(line.strip())) + '<br/>')

    lines += restaurant_end()

    return lines

def parse_stories() :
    lines = list()
    lines += restaurant_start('Flemingsberg Stories', 'Huddinge', 
                              'http://www.cafestories.se/', 
                              'https://www.openstreetmap.org/#map=19/59.22050/17.94205')
    lines += restaurant_end()
    return lines

def parse_tango(filename, weekday, tomorrow, day, month) :
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

def parse_subway(wdigit) :
    # sub of the day
    subotd = {0: 'Kalkon & skinka', 1: 'Skagenröra', 2: 'Kalkon', 3: 'Italian B.M.T', 4: 'Tonfisk', 5: 'Spicy italian', 6: 'Grillat kycklingbr&ouml;st', 7: 'Kalkon & skinka'}
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

def restaurant_start(restaurant, location, home_url, mapurl) :
    lines = list()
    lines.append('''<b><a href="{url}"> {rest}</a> (<a href="{murl}">{loc}</a>)</b><br/>'''.format(rest = restaurant, 
                                                                                                   url = home_url, 
                                                                                                   loc = location,
                                                                                                   murl = mapurl))
    lines.append('<p>')
    return lines

def restaurant_end() :
    lines = list()
    lines.append('</p>')
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
        print('\n'.join(parse_hjulet(files[restaurants.index('hjulet')], WEEKDAY, TOMORROW, WEEK)))

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

    if 'tango' in restaurants :
        print('\n'.join(parse_tango(files[restaurants.index('tango')], WEEKDAY, TOMORROW, DAY, MONTHS[MONTH])))



    print('\n'.join(page_end()))
