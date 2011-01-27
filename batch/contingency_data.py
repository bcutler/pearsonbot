import sqlite3
import os

if os.path.exists('../pearson.db'): os.remove('../pearson.db')

db = sqlite3.connect("../pearson.db")

c = db.cursor()

c.execute("""CREATE TABLE responses(gid INT, lid INT, gname TEXT, lname TEXT);""")
c.execute("""CREATE TABLE contingency(lid1 INT, lid2 INT, count INT);""")

db2 = sqlite3.connect("../../../testpilot/studies/beta_interface_2/sequence/old_interface.db")
c2 = db2.cursor()

q1 = """SELECT * from survey;"""
q2 = """SELECT * from events INNER JOIN survey WHERE events.user_id in (SELECT user_id from survey);"""

for (qrow) in c.execute(q1):
	user_id = qrow[0]
	qrow = qrow[1:]
	


# responses = [
# 	[0, 0, "os", "mac"],
# 	[0, 1, "os", "linux"],
# 	[0, 2, "os", "windows"],
# 	[1, 3, "gender", "male"],
# 	[1, 4, "gender", "female"],
# ]
# 
# contingency = [
# 	[0,3, 10],
# 	[0,4, 20],
# 	[1,3, 30],
# 	[1,4, 5],
# 	[2,3, 12],
# 	[2,4, 53],
# ]
# 
c.executemany('''INSERT INTO responses values(?,?,?,?);''', responses)
c.executemany('''INSERT INTO contingency values(?,?,?);''', contingency)
db.commit()