#!/usr/bin/env python3

import main as mn
import parser as ps

def test_read_restaurants() :
    import tempfile
    import os

    text = '''#identifier	Name	URL	Menu URL	Open Streetmap
61an	Restaurang 61:an	http://gastrogate.com/restaurang/61an/	http://gastrogate.com/restaurang/61an/page/3/	https://www.openstreetmap.org/#map=19/59.22071/17.93717
alfred	Alfreds restaurang	http://www.alfredsrestaurang.se/	http://www.alfredsrestaurang.se/	https://www.openstreetmap.org/#map=19/59.21944/17.94074
arom	Café Arom	http://aromsh.se/	http://aromsh.se/?page_id=13	http://www.openstreetmap.org/#map=18/59.21955/17.94160'''
    
    file_name = tempfile.mkstemp()[1]
    with open(file_name, 'w') as f:
        f.write(text)

    answer = [['61an', 'Restaurang 61:an', 'http://gastrogate.com/restaurang/61an/', 'http://gastrogate.com/restaurang/61an/page/3/'   , 'https://www.openstreetmap.org/#map=19/59.22071/17.93717'],
              ['alfred', 'Alfreds restaurang', 'http://www.alfredsrestaurang.se/', 'http://www.alfredsrestaurang.se/', 'https://www.openstreetmap.org/#map=19/59.21944/17.94074'],
              ['arom', 'Café Arom', 'http://aromsh.se/', 'http://aromsh.se/?page_id=13', 'http://www.openstreetmap.org/#map=18/59.21955/17.94160']]
    
    assert mn.read_restaurants(file_name) == answer
