#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 07.09.2010
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import os
from collections import defaultdict
import csv
from EveGlance.helpers import get_all_station
from EveGlance.eve_map import get_route_length

def find_all_trade_hubs(year=2013, start_month=10):
    '''
    '''
    _dump_file = "%s-%s%s-%s%s.dump"
    popular_hubs_sell = defaultdict(int)
    popular_hubs_buy = defaultdict(int)
    stationid2name = get_all_station()
    for m in xrange(start_month,13):
	for d in xrange(1,32):
		if m < 10:
			m1 = 0
		else:
			m1 = ''
		if d < 10:
			d1 = 0
		else:
			d1 = ''
		dump_file = _dump_file % (year, m1, m, d1, d)
		print "Load file:", dump_file
		if not os.path.isfile(dump_file):
			continue
		with open(dump_file) as fh:
			fh.readline()
			for i, items in enumerate(csv.reader(fh, delimiter=',', quotechar='"')):
				hubid = int(items[3])
				if hubid in stationid2name:
					hubid = stationid2name[hubid]
				bid = int(items[5])
				if bid:
					popular_hubs_buy[hubid] += 1
				else:
					popular_hubs_sell[hubid] += 1
		print "Sort data..."
		temp_results_sell = popular_hubs_sell.items()
		temp_results_buy = popular_hubs_buy.items()
		temp_results_sell.sort(key=lambda x: x[1], reverse=True)
		temp_results_buy.sort(key=lambda x: x[1], reverse=True)
		print "Current result sell:\n\n", temp_results_sell[:10], "\n\n"
		print "Current result buy:\n\n", temp_results_buy[:10], "\n\n"

    print "Save data"
    keys = set(popular_hubs_buy.keys()).union(popular_hubs_sell.keys())
    total_sell = sum(popular_hubs_sell.values()) * 1.
    total_buy = sum(popular_hubs_buy.values()) * 1. 
    with open("hubstat.dat", "w") as fh:
	    for key in keys:
	    	sell = 0
	    	buy = 0
	    	if key in popular_hubs_sell:
	    		sell = popular_hubs_sell[key]
	    	if key in popular_hubs_sell:
	    		buy = popular_hubs_buy[key]
	    	psell = 0
	    	pbuy =0
	    	if total_sell:
	    		psell = round(100 * sell/total_sell, 4)
	    	if total_buy:
	    		pbuy = round(100 * buy/total_buy, 4)
	    	buy_to_sell = 0
	    	if sell:
	    		buy_to_sell = round(buy/float(sell), 4)
	    	total = buy + sell
	    	fh.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (key, total, sell, buy, psell, pbuy, buy_to_sell))

if __name__ == '__main__':
	find_all_trade_hubs(year=2013, start_month=10)