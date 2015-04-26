#!/usr/bin/env python

import sqlite3
from bs4 import BeautifulSoup
import json

db = sqlite3.connect('./Atom.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass

cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = './Atom.docset/Contents/Resources/Documents/'

def fetch():
    with open('./atom-api.json') as _api:
        api = json.load(_api)

    _to_insert = []
    for attr, value in api['classes'].items():
        _name = attr
        _path = '%s.html' % attr
        _to_insert.append((_name, 'Class', _path))

        for method in value['classMethods']:
            _name = '%s.%s' % (attr, method['name'])
            _path = '%s.html#%s' % (attr, method['name'])
            _to_insert.append((_name, 'Method', _path))

        for method in value['instanceMethods']:
            _name = '%s::%s' % (attr, method['name'])
            _path = '%s.html#instance-%s' % (attr, method['name'])
            _to_insert.append((_name, 'Method', _path))

        if len(_to_insert) is not 1:
            cur.executemany('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', _to_insert)

        removeUnusableElement('%s%s.html' % (docpath, attr))

def removeUnusableElement(filename):
    soup = BeautifulSoup(open(filename).read())
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

fetch()
db.commit()
db.close()
