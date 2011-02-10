import sqlite3
import os
from itertools import permutations

def setup():
	if os.path.exists('../prod.db'): os.remove('../prod.db')

	db = sqlite3.connect("../prod.db")

	c = db.cursor()

	c.execute("""CREATE TABLE responses(gid INT, lid INT, gname TEXT, lname TEXT);""")
	c.execute("""CREATE TABLE contingency(lid1 INT, lid2 INT, count INT);""")
	
	return db

def connect_to_interface():
	db = sqlite3.connect("../../../testpilot/studies/beta_interface_2/sequence/data/interface_large.db")
	return db


# get all the response questions as lids.

def add_responses(response_map, c):
	gid = 0
	lid = 0

	gmap = {}
	lmap = {}
	
	for group in response_map:
		gmap[group] = gid
		responses = response_map[group]
		
		gid += 1
		
		for response in responses:
			lmap[response] = lid
			#print gid, lid, group, response
			c.execute("""INSERT INTO responses VALUES(?,?,?,?);""", (gid, lid, group, response))
			lid += 1
	
	return [gmap, lmap]

def main():
	q1 = ["less than 3 months", "3 to 6 months", "6 months to a year", "1 to 2 years", "2 to 3 years", "3 to 5 years", "More than 5 years"]
	# Primary browser
	q4 = ["No others, only Firefox", "Firefox", "Chrome", "Safari", "Opera", "Internet Explorer"]
	# gender
	q5 = ["Male", "Female"]
	#q5 = ["Female", "Male"]
	# age
	q6 = ["Under 18", "18-25", "26-35", "36-45", "46-55", "Older than 55"]
	# time spent on web
	q7 = ["< 1 hr", "1-2 hrs", "2-4 hrs", "4-6 hrs", "6-8 hrs", "8-10 hrs", "> 10 hrs"]
	# how would you describe your experience level? scale 1-10
	q8 = range(0,11)

	responses = {
		"Firefox usage": q1,
		"Primary browser":                 q4,
		"Gender":                          q5,
		"Age":                             q6,
		"Time on web":                     q7,
		"Experience Level":                q8
	}
	
	query1 = """SELECT * from survey;"""
	query2 = """SELECT * from events INNER JOIN survey WHERE events.user_id in (SELECT user_id from survey);"""
		
	qs = [1, 4, 5, 6, 7, 8]
	
	response_map = {
		1: q1,
		4: q4,
		5: q5,
		6: q6,
		7: q7,
		8: q8
	}
	
	combs = {}
	
	db = setup()
	c = db.cursor()
	
	db2 = connect_to_interface()
	c2 = db2.cursor()
	
	gmap, lmap = add_responses(responses, c)
	
	
	for (qrow) in c2.execute(query1):
		#user_id = qrow[0]
		#qrow = qrow[1:]
		# convert all the main qs.
		#print qrow[0]
		spots = [lmap[response_map[i][int(qrow[i])]] for i in qs if qrow[i] != None]
		#import sys; sys.exit()
		#print spots
		if len(spots) > 2 and len(qrow) == 15:
			#print len(qrow)
			for comb in permutations(spots, r = 2):
				if comb not in combs: combs[comb] = 0
				combs[comb] += 1
	
	for comb in sorted(combs.keys()):# sorting is easy fix for client-side bits.
		#print comb
		c.execute("""INSERT INTO contingency VALUES(?,?,?)""", (comb[0], comb[1], combs[comb]))
	
	db.commit()
	
	#print c.fetchall()

if __name__ == "__main__":
	main()