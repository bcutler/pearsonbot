from scipy.stats import chi2
from math import floor

##############################################################################
#####################              Helpers            ########################
##############################################################################

def fetch_data(term1, term2, db):
	c = db.cursor()
	c.execute('''SELECT t1.gname AS term1, 
						t2.gname AS term2, 
						t1.lname as label1, 
						t2.lname as label2, 
						contingency.count 
		FROM contingency 
			INNER JOIN responses t1 ON t1.lid = contingency.lid1 
			INNER JOIN responses t2 ON t2.lid = contingency.lid2 
		WHERE 
			term1 = ? AND term2 = ?;''', 
		(term1, term2))
	data = c.fetchall()
	return data

def to_contingency_table(data, normalized = False):
	
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
	
	if normalized:
		data_obj = [[(c / float(sum(r)))*100  for c in r]    for r in data_obj]
	
	row_labels = sorted([(v,k) for k,v in row_labels.items()])
	row_labels = [k for v, k in row_labels]
	
	col_labels = sorted([(v, k) for k,v in col_labels.items()])
	col_labels = [k for v,k in col_labels]
	
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
	obj['col_totals'] = [sum(row[i] for row in data_obj) \
				for i, col in enumerate(data_obj[0])]
	obj['n'] = sum(obj['row_totals'])
	
	obj['p_value'] = chisq_test(obj)
	
	return obj

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
	
	return floor(chi2.cdf(chisq_stat, df) * 100 ) / 100.
