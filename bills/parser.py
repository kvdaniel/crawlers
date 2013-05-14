#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import re

import lxml
import utils
from settings import NUM_PAGES, MAX_PAGE, LIST_DATA, BASEURL, X

def extract(columns):
    data = []
    for j, c in enumerate(columns):
        if j==1:
            data.append(re.findall(r'[0-9]+', c.xpath('img/@src')[0])[0])
            data.append(c.xpath('a/text()')[0])
            data.append(re.findall(r'\w+', c.xpath('a/@href')[0])[2])
        elif j==6:
            url = c.xpath('img/@onclick')
            if url:
                d = '1'
            else:
                d = '0'
            data.append(d)
        else:
            data.append(c.xpath('text()')[0].strip())
    return data

def get_data(i, f):
    fn = '%s/%s.html' % (LIST_DIR, i)
    page = utils.read_webpage(fn)
    rows = utils.get_elems(page, X['table'])

    for r in rows:
        columns = r.xpath(X['columns'])
        if len(columns)==8:
            f.write('"')
            f.write('","'.join(extract(columns)).encode('utf-8'))
            f.write('"\n')
    print fn

if __name__=='__main__':
    with open(LIST_DATA, 'wa') as f:
        for i in range(MAX_PAGE/NUM_PAGES+1):
            get_data(i+1, f)