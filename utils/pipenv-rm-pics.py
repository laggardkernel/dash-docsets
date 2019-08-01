# -*- coding: utf-8 -*-
# @Author: wyh
# @Date:   2018-08-10 20:09:19
# @Last Modified by:   laggardkernel
# @Last Modified time: 2018-10-19 19:25:16

import sys
import os
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from lxml import etree


# def remove_pics(filename):
#     # doc = pq(filename=filename, parser="html")
#     # doc = pq(filename=filename)
#     with open(filename, "r") as f:
#         doc = pq(f.read(), parser="html")
#     # doc = pq(etree.parse(filename), parser="html")

#     remove_list = [
#         "div.section > h1 + img",
#         "div.section > h1 ~ a.image-reference",
#         "body div.footer + a",
#     ]
#     for item in remove_list:
#         temp = doc.find(item)
#         if temp:
#             print(temp)
#             temp.remove()

#     # if os.path.split(filename)[-1] in ['index.html', 'index.htm']:
#     #     temp = doc.find('body div h1').siblings().filter('a')
#     #     if temp:
#     #         print(temp)
#     #         temp.remove()

#     with open(filename, "w+") as f:
#         f.write(str(doc.__html__()))
#     #     f.write(str(doc.outer_html()))
#     # print(str(doc.__html__()))


def remove_pics(filename):
    with open(filename, "r+") as f:
        soup = BeautifulSoup(f, "lxml")

    # print(str(soup))
    remove_list = [
        "div.section > h1 + img",
        "div.section > h1 ~ a.image-reference",
        "body div.footer + a",
    ]
    for selector in remove_list:
        r = soup.select(selector)
        if len(r) > 0:
            for item in r:
                print(item)
                item.decompose()

    with open(filename, "w") as f:
        f.write(str(soup))


def traverse_process(dirname):
    for item in os.listdir(dirname):
        filename = os.path.join(dirname, item)
        if os.path.isfile(filename) and filename.split(".")[-1] in ["html", "htm"]:
            print("\n", filename)
            remove_pics(filename)
        elif os.path.isdir(filename):
            traverse_process(filename)
        else:
            pass


if __name__ == "__main__":
    dirs = ["./html"]
    for dirname in dirs:
        traverse_process(dirname)

    # remove_pics('./html/user/intro.html')
    # remove_pics('./html/index.html')

# div.footer {width:auto; max-width:940px} div.document {max-width:940px; width: auto} div.related {display:none;} div.sphinxsidebar {display:none;} a.headerlink {display:none;} .document {max-width:none !important} div.bodywrapper {margin: 0 0 0 0px;}
# div.body {max-width:none !important} div.footer {text-align: center;} a.github {display:none;}
# doc2dash --name Requests --index-page index.html -A ./_build/html -j -v
