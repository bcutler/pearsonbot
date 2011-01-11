from django.db import connection, transaction

def get_group_names():
	c = connection.cursor()
	c.execute("""SELECT DISTINCT gname FROM responses;""")
	d = c.fetchall()
	d = [i for (i,) in d]
	return d

# def get_contingency_table(term1, term2):
# 	c = connection.cursor()
# 	c.execute('''SELECT t1.gname AS term1, 
# 						t2.gname AS term2, 
# 						t1.lname as label1, 
# 						t2.lname as label2, 
# 						contingency.count 
# 		FROM contingency 
# 			INNER JOIN responses t1 ON t1.lid = contingency.lid1 
# 			INNER JOIN responses t2 ON t2.lid = contingency.lid2 
# 		WHERE 
# 			(t1.gname = %s AND t2.gname = %s) OR
# 			(t1.gname = %s AND t2.gname = %s);''', 
# 		(term1, term2, term2, term1))
# 	data = c.fetchall()
# 	#print data
# 	
# 	# determine what the feature order is.
# 	# d = data[0]
# 	
# 	nrows = len(set([l1 for t1, t2, l1, l2, c in data if t1 == term1]))
# 	if nrows == 0:
# 		nrows = len(set([l2 for t1, t2, l1, l2, c in data if t2 == term1]))
# 	ncols = len(set([l2 for t1, t2, l1, l2, c in data if t2 == term2]))
# 	if ncols == 0:
# 		ncols = len(set([l1 for t1, t2, l1, l2, c in data if t1 == term2]))
# 	#print len(set([l1 for t1, t2, l1, l2, c in data if t1 == term1]))
# 	data_obj = [[0 for j in xrange(ncols)] for i in xrange(nrows)]
# 	row_labels = {}
# 	col_labels = {}
# 	
# 	for t1, t2, l1, l2, c in data:
# 		if t1 == term1:
# 			lab1 = l1
# 		elif t2 == term1:
# 			lab1 = l2
# 		if t1 == term2:
# 			lab2 = l1
# 		elif t2 == term2:
# 			lab2 = l2
# 		if lab1 not in row_labels: row_labels[lab1] = len(row_labels)
# 		if lab2 not in col_labels: col_labels[lab2] = len(col_labels)
# 		#print t1, t2, l1, l2, lab1, lab2, c, nrows, ncols, data_obj
# 		data_obj[row_labels[lab1]][col_labels[lab2]] = c
# 	
# 	obj = {'labels':
# 			{
# 				"row": term1,
# 				"col":term2,
# 				"row_labels": row_labels,
# 				"col_labels": col_labels,
# 			},
# 			'data': data_obj
# 	}
# 	
# 	obj['row_totals'] = [sum(r) for r in data_obj]
# 	obj['col_totals'] = [sum(row[i] for row in data_obj) for i, col in enumerate(data_obj[0])]
# 	
# 	return obj

#
def get_contingency_table(term1, term2):
	c = connection.cursor()
	c.execute('''SELECT t1.gname AS term1, 
						t2.gname AS term2, 
						t1.lname as label1, 
						t2.lname as label2, 
						contingency.count 
		FROM contingency 
			INNER JOIN responses t1 ON t1.lid = contingency.lid1 
			INNER JOIN responses t2 ON t2.lid = contingency.lid2 
		WHERE 
			t1.lname = %s AND t2.lname = %s;''', 
		(term1, term2))
	data = c.fetchall()
	#print data
	
	# determine what the feature order is.
	# d = data[0]
	
	nrows = len(l1 for t1, t2, l1, l2, c in data)
	ncols = len(l2 for t1, t2, l1, l2, c in data)
	
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
	
	return obj

def chisq_test(table):
	"""FINISH THIS"""
	row_totals = [sum(row) for row in table]
	#print "rows", row_totals
	col_totals = [sum(row[i] for row in table) for i, col in enumerate(table[0])]
	#print 'cols', col_totals
	tot = sum(row_totals)
	#print 'tot', tot
	chisq_stat = sum(sum((table[j][i] - c*r/float(tot)**2) / tot for j,r in enumerate(row_totals)) for i,c in enumerate(col_totals))
	#print row_totals, col_totals, tot
	df = (len(row_totals) - 1) * (len(col_totals)-1)
	return chisq_stat