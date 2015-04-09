#!/usr/bin/env python

import re, os, sqlite3
from bs4 import BeautifulSoup
from urllib import parse

db = sqlite3.connect('./Atom.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass

cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = './Atom.docset/Contents/Resources/Documents/'

def fetch(f):
    filename = os.path.join(root, f)
    page = open(filename).read()
    soup = BeautifulSoup(page)
    _path = filename.replace(docpath, '')
    _to_insert = []

    _Class = os.path.splitext(f)[0]
    _to_insert.append((_Class, 'Class', _path))

    for method in soup.select('.method-signature'):
        _name = method['name'].replace('instance-', '')
        _operator = method.find('span', { 'class': 'operator' }).contents[0].strip()

        print(_path, _operator, _name)
        _to_insert.append((_Class + _operator + _name, 'Method', _path + '#'+ method['name']))

    if len(_to_insert) is not 1:
        cur.executemany('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', _to_insert)

    _to_remove = [
            soup.find('div', { 'class': 'top-bar' }),
            soup.find('form'),
            soup.find('footer'),
            soup.find('div', { 'class': 'sidebar' }),
            ]

    for r in _to_remove:
        if r:
            r.extract()

    with open(filename, 'wb') as file:
        file.write(soup.prettify('utf-8'))

for root, dirs, files in os.walk(docpath):
    for f in files:
        if f.endswith('.html'):
            fetch(f)

db.commit()
db.close()
