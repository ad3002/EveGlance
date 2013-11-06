#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 07.09.2010
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import simplejson
from EveGlance.helpers import make_request

def get_blueprint(settings):
	'''
	'''
	url = "http://api.clonerworks.com/api/blueprint-calc/%(itemid)s/%(ME)s/%(PE)s/%(PES)s/%(PEM)s/%(ISL)s/%(MM)s"
	data = {
	'itemid': settings["itemid"],
	'ME': settings["ME"],
	'PE': settings["PE"],
	'PES': settings["PES"],
	'PEM': settings["PEM"],
	'ISL': settings["ISL"],
	'MM': settings["MM"],
	}
	_url = url % data
	data = simplejson.loads(make_request(_url))
	print data.keys()

settings = {
  	"itemid": 12431,
  	"ME": -4,
  	"PE": -4,
  	"PES": 5,
  	"PEM": 65,
  	"ISL": 5,
  	"MM": 12,
  }

get_blueprint(settings)