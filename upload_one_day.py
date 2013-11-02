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
from EveGlance.scrapper import load_dump, get_settings, convert_and_clean_dump


def load_dumps_to_json(year=2013, m=1, d=12):
    """
    Upload data to server by date.
    @param year: year (default 2013)
    @param m: month
    @param d: day
    """
    file_name = "/storage1/akomissarov/em/%s-%s%s-%s%s.dump"
    output_file_name = "/storage1/akomissarov/em/%s-%s%s-%s%s.dat"
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
    convert_and_clean_dump(input_fn, output_fn)


if __name__ == '__main__':
    settings = get_settings()
    parser = argparse.ArgumentParser(description='Upload file by day and month.')
    parser.add_argument('-m','--month', help='Month', required=True)
    parser.add_argument('-d','--day', help='Day', required=True)
    args = vars(parser.parse_args())
    m = int(args["month"])
    d = int(args["day"])
    load_dumps_to_json(m=m, d=d)
