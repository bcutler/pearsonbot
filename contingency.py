from flask import Flask, render_template, request
from helpers import *

import sqlite3
import json

##############################################################################
#####################               Setup                #####################
##############################################################################

app = Flask(__name__)

##############################################################################
#####################            Controllers             #####################
##############################################################################

@app.route('/')
def index():
	db = sqlite3.connect('prod.db')
	groups = get_group_names(db)
	return render_template("index.html", groups = groups)

@app.route('/compare/')
def compare():
	term1 = request.args.get('term1')
	term2 = request.args.get('term2')
	print "HI!"
	db = sqlite3.connect('prod.db')
	table = fetch_data(term1, term2, db)
	table = to_contingency_table(table)
	#table = get_protovis_treemap(term1, term2)
	#print table
	#statistic = chisq_test(table)
	
	#table = pformat(table)
	#print table
	res = json.dumps(table)
	#print res
	return res

if __name__ == '__main__':
    app.run(debug=True)