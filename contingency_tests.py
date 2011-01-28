import os
import contingency
import unittest
import tempfile
import helpers
import sqlite3

class PearsonBotTests(unittest.TestCase):
	
	def setUp(self):
		self.db_fd, contingency.app.config['DATABASE'] = tempfile.mkstemp()
		self.app = contingency.app.test_client()
		contingency.init_db()
		contingency.test_data()
		######## Reference objects ############
		self.data_obj = {
			'labels':
				{
					'row': u'os',
					'col': u'gender',
					'row_labels': {u'mac':0, u'windows':1, u'linux':2},
					'col_labels': {u'male':0, u'female':1}
				},
			'data':
				[
					[10,20],
					[30,5],
					[12,53]
				],
			'row_totals': [30,35,65],
			'col_totals': [52,78],
			'n': 130,
			'p_value':.99
		}
		self.db = sqlite3.connect(contingency.app.config['DATABASE'])
		
	
	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(contingency.app.config['DATABASE'])
	
	def test_chisq_test(self):
		p_value = helpers.chisq_test(self.data_obj)
		self.assertEqual(.99, p_value) 
	
	def test_contingency_table(self):
		data = helpers.fetch_data('os', 'gender', self.db)
		table = helpers.to_contingency_table(data)
		self.assertEqual(table, self.data_obj)

if __name__ == "__main__":
	unittest.main()