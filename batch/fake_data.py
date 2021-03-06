import sqlite3
import os

if os.path.exists('../fake.db'): os.remove('../fake.db')

db = sqlite3.connect("../fake.db")

c = db.cursor()

c.execute("""CREATE TABLE responses(gid INT, lid INT, gname TEXT, lname TEXT);""")
c.execute("""CREATE TABLE contingency(lid1 INT, lid2 INT, count INT);""")

responses = [
	[0, 0, "os", "mac"],
	[0, 1, "os", "linux"],
	[0, 2, "os", "windows"],
	[1, 3, "gender", "male"],
	[1, 4, "gender", "female"],
]

contingency = [
	[0,3, 10],
	[0,4, 20],
	[1,3, 30],
	[1,4, 5],
	[2,3, 12],
	[2,4, 53],
	[3,0, 10],
	[4,0, 20],
	[3,1, 30],
	[4,1, 5],
	[3,2, 12],
	[4,2, 53],
]

c.executemany('''INSERT INTO responses values(?,?,?,?);''', responses)
c.executemany('''INSERT INTO contingency values(?,?,?);''', contingency)
db.commit()