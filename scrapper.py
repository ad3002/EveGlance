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
import simplejson
from lxml import objectify
import yaml
import re
import os
from datetime import datetime
import calendar

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
    print "Load:", url
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, error:
        print error.fp.read()
    content = page.read()
    return content


def parse_items_to_json(settings):
    """
    """
    url = settings["eve_central"]["url_items"]
    output_file = settings["eve_central"]["items_json_file"]
    data = make_request(url)
    data = data.split("\n")[2:]
    last_line = data[-3]
    total = int(re.findall("(\d+)", last_line)[0])
    print last_line, total
    result = []
    for i, line in enumerate(data):
        items = line.strip().split("|")
        if len(items) != 8:
          continue
        items = [x.strip() for x in items]

        def unknown_item(x):
            if x:
                return x
            else:
                return -1

        items = map(unknown_item, items)
        print items
        (typeid, typename, typeclass, size, published, marketgroup, groupid, raceid) = items
        d = {
          "typeid": int(typeid),
          "typename": typename,
          "typeclass": typeclass,
          "size": float(size),
          "published": int(published),
          "marketgroup": int(marketgroup),
          "groupid": int(groupid),
          "raceid": int(raceid)
        }
        result.append(simplejson.dumps(d))
    print "Join data"
    data = "\n".join(result)
    print "Save data"
    with open(output_file, "w") as fh:
        fh.write(data)
    upload_command = "mongoimport --upsert -d EM -c Items %s " % output_file
    print upload_command
    os.system(upload_command)


def convert_duration(duration):
    """
    """
    items = re.findall("(\d+).*?(\d+):(\d+):(\d+)", duration)[0]
    items = map(int, items)
    (d, h, m, s) = items
    return s + m * 60 + h * 60 * 60 + d * 60 * 60 * 24
   
def load_dump(dump_file):
    """
    "orderid","regionid","systemid","stationid","typeid","bid","price","minvolume","volremain","volenter","issued","duration","range","reportedby","reportedtime"
    """
    with open(dump_file) as fh:
        data = fh.readlines()[1:]
    result = []
    for line in data:
        items = line.strip().split('","')
        try:
          assert len(items) == 15
        except:
          print items
          exit()



        date_object = datetime.strptime(items[10], '%Y-%m-%d %H:%M:%S')
        issued = calendar.timegm(date_object.utctimetuple())

        duration = convert_duration(items[11])

        date_object = datetime.strptime(items[14][:-1], '%Y-%m-%d %H:%M:%S.%f')
        reportedtime = calendar.timegm(date_object.utctimetuple())


        d = {
          "orderid": int(items[0][1:]),
          "regionid": int(items[1]),
          "systemid": int(items[2]),
          "stationid": int(items[3]),
          "typeid": int(items[4]),
          "bid": int(items[5]),
          "price": float(items[6]),
          "minvolume": int(items[7]),
          "volremain": int(items[8]),
          "volenter": int(items[9]),
          "issued": issued,
          "duration": duration,
          "range": int(items[12]),
          "reportedby": int(items[13]),
          "reportedtime": reportedtime,
        }

        print  d


settings_file = "/home/akomissarov/Dropbox/EveGlance/settings.yaml"
with open(settings_file) as fh:
    settings = yaml.load(fh)
# parse_items_to_json(settings)

dump_file = "/storage1/akomissarov/em/2013-02-05.dump"
load_dump(dump_file)

# url = settings["url_onpath"]

# data = make_request(url)

# root = objectify.fromstring(data)
# print min([x.price for x in root.quicklook.sell_orders.iterchildren()])
# print max([x.price for x in root.quicklook.buy_orders.iterchildren()])