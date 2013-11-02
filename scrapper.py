#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 07.09.2010
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com
"""
API to eve market
"""
import argparse
import urllib2
import simplejson
from lxml import objectify
import yaml
import re
import os
from datetime import datetime
import calendar
import csv

def make_request(url):
    """Makes a request to external resource.
    @param url: url
    """

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
    Download item index, parse it, and upload to MongoDB.
    @settings eve_central.url_items: url to items file
    @settings eve_central.items_json_file: output file with json dump
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
    Convert bid duration to seconds.
    """
    items = re.findall("(\d+).*?(\d+):(\d+):(\d+)", duration)[0]
    items = map(int, items)
    (d, h, m, s) = items
    return s + m * 60 + h * 60 * 60 + d * 60 * 60 * 24


def load_dump(dump_file, output_file, mongo=False):
    """
    Convert dump file to json and save it into file.
    Data fields:
        "orderid","regionid","systemid","stationid","typeid","bid","price","minvolume","volremain","volenter","issued","duration","range","reportedby","reportedtime"
    """
    print "Load data from", dump_file
    with open(dump_file) as fh:
        data = fh.readlines()[1:]
    result = []
    print "Parse data from", dump_file
    for i, line in enumerate(data):
        line = line.strip()
        if not line:
            continue
        print i, "\r",
        items = line.split('","')
        try:
            assert len(items) == 15
        except:
            print items
            exit()

        date_object = datetime.strptime(items[10], '%Y-%m-%d %H:%M:%S')
        issued = calendar.timegm(date_object.utctimetuple())

        duration = convert_duration(items[11])

        if "." in items[14]:
            date_object = datetime.strptime(items[14][:-1], '%Y-%m-%d %H:%M:%S.%f')
        else:
            date_object = datetime.strptime(items[14][:-1], '%Y-%m-%d %H:%M:%S')
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

        result.append(simplejson.dumps(d))
    print
    print "Join data"
    data = "\n".join(result)
    print "Save data"
    with open(output_file, "w") as fh:
        fh.write(data)
    if mongo:
        print "Upload data"
        upload_command = "mongoimport --upsert -d EM -c History %s " % output_file
        print upload_command
        os.system(upload_command)

def convert_and_clean_dump(dump_file, output_file):
    """
    Read dump file, sort it by orderid, and save as tab delimietd file.
    Data fields:
        "orderid","regionid","systemid","stationid","typeid","bid","price","minvolume","volremain","volenter","issued","duration","range","reportedby","reportedtime"
    """
    print "Load data from", dump_file
    dataset = []
    with open(dump_file) as fh:
        for items in csv.reader(fh, delimiter=',', quotechar='"')]:
          d = [
            int(items[0]),
            int(items[1]),
            int(items[2]),
            int(items[3]),
            int(items[4]),
            int(items[5]),
            float(items[6]),
            int(items[7]),
            int(items[8]),
            int(items[9]),
            items[10],
            items[11],
            int(items[12]),
            int(items[13]),
            items[14],
          ]
          dataset.append(d)


    print "Parse data from", dump_file
    k = 0
    for i, line in enumerate(data):
        line = line.strip()
        if not line:
            continue
        print i, k, "\r",
        items = line.split('","')
        try:
            assert len(items) == 15
        except:
            print items
            exit()
        if not items[3] == '60003760':
            continue
        k += 1
        date_object = datetime.strptime(items[10], '%Y-%m-%d %H:%M:%S')
        issued = calendar.timegm(date_object.utctimetuple())
        duration = convert_duration(items[11])
        if "." in items[14]:
            date_object = datetime.strptime(items[14][:-1], '%Y-%m-%d %H:%M:%S.%f')
        else:
            date_object = datetime.strptime(items[14][:-1], '%Y-%m-%d %H:%M:%S')
        reportedtime = calendar.timegm(date_object.utctimetuple())


        d = [
          int(items[0][1:]),
          int(items[1]),
          int(items[2]),
          int(items[3]),
          int(items[4]),
          int(items[5]),
          float(items[6]),
          int(items[7]),
          int(items[8]),
          int(items[9]),
          issued,
          duration,
          int(items[12]),
          int(items[13]),
          reportedtime,
        ]

        result.append(d)
    print
    print "Print sort data"
    result.sort()
    print "Format data"
    result = ["%s\n" % "\t".join(map(str, x)) for x in result]
    with open(output_file, "w") as fh:
        fh.writelines(result)


def download_daily_dumps(year=2013):
    """
    Download daily dumps from eve central.
    """
    url = "http://eve-central.com/dumps/%s-%s%s-%s%s.dump.gz"
    for m in xrange(0,13):
      for d in xrange(0,32):
        if m < 10:
          m1 = 0
        else:
          m1 = ''
        if d < 10:
          d1 = 0
        else:
          d1 = ''
        purl = url % (year, m1, m, d1, d)
        command = "nohup wget -c %s > /dev/null &" % purl
        print command
        os.system(command)

def get_settings():
    """
    Load settings.
    """
    settings_file = "/home/akomissarov/Dropbox/EveGlance/settings.yaml"
    with open(settings_file) as fh:
        settings = yaml.load(fh)
    return settings


def load_dumps_to_json(year=2013, m_from=1, m_to=12):
    """
    """
    file_name = "/storage1/akomissarov/em/%s-%s%s-%s%s.dump"
    output_file_name = "/storage1/akomissarov/em/%s-%s%s-%s%s.json"
    for m in xrange(m_from,m_to+1):
      for d in xrange(1,32):
        print "Month", m, "Day", d
        if m < 10:
          m1 = 0
        else:
          m1 = ''
        if d < 10:
          d1 = 0
        else:
          d1 = ''
        input_fn = file_name % (year, m1, m, d1, d)
        output_fn = output_file_name % (year, m1, m, d1, d)
        if os.path.isfile(output_fn):
            print "Skipped:", file_name
            continue
        load_dump(input_fn, output_fn, mongo=False)

#if __name__ == '__main__':
#
#    settings = get_settings()
#
#    parser = argparse.ArgumentParser(description='Do sometings.')
#    parser.add_argument('-i','--input', help='Input dump file', required=True)
#    parser.add_argument('-m','--mongo', help='Upload to mongo', required=False, default=False)
#    args = vars(parser.parse_args())
#    dump_file = args["input"]
#    mongo = args["mongo"]
#    output_file = dump_file.split(".")[0] + ".json"
#    load_dump(dump_file, output_file, mongo=mongo)

if __name__ == '__main__':

    settings = get_settings()
    parser = argparse.ArgumentParser(description='Do sometings.')
    parser.add_argument('-f','--month_from', help='Month from', required=True)
    parser.add_argument('-t','--month_to', help='Month to', required=True)
    args = vars(parser.parse_args())
    mf = int(args["month_from"])
    mt = int(args["month_to"])
    load_dumps_to_json(year=2013, m_from=mf, m_to=mt)

# root = objectify.fromstring(data)
# print min([x.price for x in root.quicklook.sell_orders.iterchildren()])
# print max([x.price for x in root.quicklook.buy_orders.iterchildren()])