from django.db import connections, transaction
from math import pi, sqrt, factorial, e, floor
from operator import mul
from scipy.stats import chi2


def get_group_names():
	c = connections['default'].cursor()
	c.execute("""SELECT DISTINCT gname FROM responses;""")
	d = c.fetchall()
	d = [i for (i,) in d]
	return d

def fetch_data(term1, term2, db="default"):
	c = connections[db].cursor()
	c.execute('''SELECT t1.gname AS term1, 
						t2.gname AS term2, 
						t1.lname as label1, 
						t2.lname as label2, 
						contingency.count 
		FROM contingency 
			INNER JOIN responses t1 ON t1.lid = contingency.lid1 
			INNER JOIN responses t2 ON t2.lid = contingency.lid2 
		WHERE 
			term1 = %s AND term2 = %s;''', 
		(term1, term2))
	data = c.fetchall()
	return data

def compute_residuals(table_obj):
	
	pass
	

def to_contingency_table(data):
	
	#data = fetch_data(term1, term2)
	term1 = [t1 for t1, t2, l1, l2, c in data][0]
	term2 = [t2 for t1, t2, l1, l2, c in data][0]
	nrows = len(set([l1 for t1, t2, l1, l2, c in data]))
	ncols = len(set([l2 for t1, t2, l1, l2, c in data]))
	
	data_obj = [[0 for j in xrange(ncols)] for i in xrange(nrows)]
	
	row_labels = {}
	col_labels = {}
	
	for t1, t2, l1, l2, c in data:
		if l1 not in row_labels: row_labels[l1] = len(row_labels)
		if l2 not in col_labels: col_labels[l2] = len(col_labels)
		data_obj[row_labels[l1]][col_labels[l2]] = c
	
	obj = {'labels':
			{
				"row": term1,
				"col":term2,
				"row_labels": row_labels,
				"col_labels": col_labels,
			},
			'data': data_obj
	}
	
	obj['row_totals'] = [sum(r) for r in data_obj]
	obj['col_totals'] = [sum(row[i] for row in data_obj) for i, col in enumerate(data_obj[0])]
	obj['n'] = sum(obj['row_totals'])
	
	obj['p_value'] = chisq_test(obj)
	
	return obj

def get_protovis_treemap(term1, term2):
	data = fetch_data(term1, term2)
	
	data_obj = {}
	for (t1, t2, l1, l2, c) in data:
		if l1 not in data_obj: data_obj[l1] = {}
		data_obj[l1][l2] = c
	
	return data_obj

######### Calculating the chi-square statistic. ##########

## NEVERMIND.  We're just going to go with

# def factorial(n):
#     return reduce(mul, range(1, n + 1), 1) # the "1" initial value allows it to work for 0

# def pos_halfinteger_gamma(n):
# 	"""expects n = k / 2 here."""
# 	n = floor(n)
# 	return sqrt(pi) * factorial(2*n) / float((2**(2*n) * factorial(n)))
# 
# def pchisq(x,df):
# 	return (x**(df/2. - 1) * e**(-x / 2.)) / (2**(df/2.) * pos_halfinteger_gamma(df/2.))
# 
# pchisq(4,2)

def chisq_test(data_obj):
	row_totals = data_obj['row_totals']
	col_totals = data_obj['col_totals']
	n = data_obj['n']
	
	chisq_stat = 0
	for i,r in enumerate(row_totals):
		for j, c in enumerate(col_totals):
			observed = data_obj['data'][i][j]
			expected = r*c / float(n)
			chisq_stat += (observed - expected)**2 / expected
	
	df = (len(row_totals) - 1) * (len(col_totals)-1)
	print chisq_stat, "!!!"
	return chi2.cdf(chisq_stat, df)

# def chisq_test(table):
# 	"""FINISH THIS"""
# 	row_totals = [sum(row) for row in table]
# 	#print "rows", row_totals
# 	col_totals = [sum(row[i] for row in table) for i, col in enumerate(table[0])]
# 	#print 'cols', col_totals
# 	tot = sum(row_totals)
# 	#print 'tot', tot
# 	chisq_stat = sum(sum((table[j][i] - c*r/float(tot)**2) / tot for j,r in enumerate(row_totals)) for i,c in enumerate(col_totals))
# 	#print row_totals, col_totals, tot
# 	df = (len(row_totals) - 1) * (len(col_totals)-1)
# 	return chisq_stat