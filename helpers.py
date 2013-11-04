#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 07.09.2010
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import urllib2
import yaml
import csv
import simplejson

def get_settings():
    """
    Load settings.
    """
    settings_file = "/home/akomissarov/Dropbox/EveGlance/settings.yaml"
    with open(settings_file) as fh:
        settings = yaml.load(fh)
    return settings

def get_all_station():
  '''
  STATIONID;SECURITY;DOCKINGCOSTPERVOLUME;MAXSHIPVOLUMEDOCKABLE;OFFICERENTALCOST;OPERATIONID;STATIONTYPEID;CORPORATIONID;SOLARSYSTEMID;CONSTELLATIONID;REGIONID;STATIONNAME;X;Y;Z;REPROCESSINGEFFICIENCY;REPROCESSINGSTATIONSTAKE;REPROCESSINGHANGARFLAG
  '''
  file_name = "staStations.csv"
  result = {}
  with open(file_name) as fh:
    fh.readline()
    for i, items in enumerate(csv.reader(fh, delimiter=';')):
      STATIONID = int(items[0])
      SECURITY = float(items[1])
      STATIONNAME = items[11]
      result[STATIONID] = STATIONNAME
  return result


def get_all_items(settings):
  all_items = []
  with open("items.json") as fh:
    for line in fh:
      all_items.append(simplejson.loads(line))
  return all_items

def get_mean(data):
    '''
    Calculate mean for given data.
    '''
    if len(data) == 0:
      return 0
    return sum(data)*1.0/len(data)

def make_request(url, verbose=False):
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
    if verbose:
        print "Load:", url
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, error:
        print error.fp.read()
    content = page.read()
    return content