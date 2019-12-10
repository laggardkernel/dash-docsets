# -*- coding: utf-8 -*-
# @Author: laggardkernel
# @Date:   2018-10-16 12:14:01
# @Last Modified by:   laggardkernel
# @Last Modified time: 2018-10-16 12:35:03

import sys
import os
import re
from pyquery import PyQuery as pq


def remove_pics(filename):
    doc = pq(filename=filename)
    # temp = doc.find('body div h1 + img')
    # if temp:
    #     print(temp)
    #     temp.remove()
    temp = doc.find('body div.footer + a')
    if temp:
        print(temp)
        temp.remove()
    # if os.path.split(filename)[-1] in ['index.html', 'index.htm']:
    #     temp = doc.find('body div h1').siblings().filter('a')
    #     if temp:
    #         print(temp)
    #         temp.remove()
    with open(filename, 'w+') as f:
        f.write(doc.html())


def relatify_links(filename):
    doc = pq(filename=filename)
    links = doc.find('a.reference.external')
    print(links)
    print(len(links))
    for item in links:
        item = pq(item)
        if item.attr('href'):
            m = re.match(r'^http[s]?://docs\.pytest\.org/en/[^/]+?/(.+?)$', item.attr('href'))
            if m:
                print(item)
                item.attr('href', m.group(1))

    with open(filename, 'w+') as f:
        f.write(doc.html())


if __name__ == '__main__':
    dirs = ['./html', './html/announce', './html/example', './html/proposals']
    for dirname in dirs:
        for item in os.listdir(dirname):
            filename = os.path.join(dirname, item)
            if os.path.isfile(filename) and filename.split('.')[-1] in ['html', 'htm']:
                print('\n', filename)
                relatify_links(filename)

    # remove_pics('./html/user/intro.html')
    # remove_pics('./html/index.html')

# div.footer {width:auto; max-width:940px} div.document {max-width:940px; width: auto} div.related {display:none;} div.sphinxsidebar {display:none;} a.headerlink {display:none;} .document {max-width:none !important} div.bodywrapper {margin: 0 0 0 0px;}
# div.body {max-width:none !important} div.footer {text-align: center;} a.github {display:none;}
# doc2dash --name Requests --index-page index.html -A ./_build/html -j -v
