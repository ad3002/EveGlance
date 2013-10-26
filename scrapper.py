#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 07.09.2010
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com
"""
API to eve market
"""
import urllib2
from lxml import objectify
import yaml

def make_request(url):
        """Makes a request to external resource."""
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Accept-Encoding': 'none',
              'Accept-Language': 'en-US,en;q=0.8',
              'Connection': 'keep-alive'
        }
        req = urllib2.Request(url, headers=hdr)
        print url
        try:
            page = urllib2.urlopen(req)
        except urllib2.HTTPError, error:
            print error.fp.read()
        content = page.read()
        return content

settings_file = "settings.yaml"
with open(settings_file) as fh:
    settings = yaml.load(fh)

url = settings["url_onpath"]

data = make_request(url)

root = objectify.fromstring(data)
print min([x.price for x in root.quicklook.sell_orders.iterchildren()])
print max([x.price for x in root.quicklook.buy_orders.iterchildren()])