#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 07.09.2010
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com
"""
Basic finance functions
"""
import math


def get_continuously_compounded_interest(M, r, t):
	"""
	"""
	return M * math.e ** (r * t)

if __name__ == '__main__':
	print get_continuously_compounded_interest(100, 0.1, 2)