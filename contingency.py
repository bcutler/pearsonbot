from contextlib import closing
from flask import Flask, render_template, request, g
from helpers import *

from pprint import pprint
import sqlite3
import json

##############################################################################
#####################               Setup                #####################
##############################################################################

app = Flask(__name__)

DATABASE = 'prod.db'
DEBUG = True
#SECRET_KEY = 'development key'
#USERNAME = 'admin'
#PASSWORD = 'default'

app.config.from_object(__name__)

##############################################################################
#####################             Database               #####################
##############################################################################

def connect_db():
	"""Returns a new connection to the database."""
	return sqlite3.connect(app.config['DATABASE'])

def sql(fname):
	with closing(connect_db()) as db:
		with app.open_resource(fname) as f:
			db.cursor().executescript(f.read())
		db.commit()

def init_db():
	sql("schema.sql")

def test_data():
	sql("test_data.sql")

##############################################################################
#####################            Controllers             #####################
##############################################################################

@app.before_request
def before_request():
	g.db = connect_db()

@app.after_request
def after_request(response):
	g.db.close()
	return response

@app.route('/')
def index():
	c = g.db.execute("""SELECT DISTINCT gname FROM responses;""")
	groups = [i for (i,) in c.fetchall()]
	return render_template("index.html", groups = groups)

@app.route('/compare/')
def compare():
	term1 = request.args.get('term1')
	term2 = request.args.get('term2')
	normalized = request.args.get('normalized') == "true"
	print "normalized?", normalized
	table = fetch_data(term1, term2, g.db)
	table = to_contingency_table(table, normalized = normalized)
	pprint(table)
	res = json.dumps(table)
	return res

if __name__ == '__main__':
    app.run(debug=True)