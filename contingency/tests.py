"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import os
import sys

ROOT = lambda base : os.path.join(os.path.dirname(__file__), base).replace('\\','/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append(ROOT("../"))
print ROOT("../")

import unittest
from django.db import connections
from helpers import *
import sqlite3

rs = to_contingency_table(fetch_data("os", "gender", db="default"))

class ContingencyHelperTest(unittest.TestCase):
	
	resultset = rs
	
	def test_row_totals(self):
		self.assertEqual(self.resultset['row_totals'], [30, 35, 65])
	
	# def test_col_totals(self):
	# 	pass
	# 
	# def test_table_vals(self):
	# 	pass
	# 
	# def test_row_labels(self):
	# 	pass
	# 
	# def test_col_labels(self):
	# 	pass

if __name__ == "__main__":
	unittest.main()
	