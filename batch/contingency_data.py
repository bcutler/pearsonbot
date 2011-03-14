import sqlite3
import os
import shelve
from itertools import permutations



def setup():
	if os.path.exists('../prod.db'): os.remove('../prod.db')

	db = sqlite3.connect("../prod.db")

	c = db.cursor()

	c.execute("""CREATE TABLE responses(gid INT, lid INT, gname TEXT, lname TEXT);""")
	c.execute("""CREATE TABLE contingency(lid1 INT, lid2 INT, count INT);""")
	
	return db

def connect_to_interface():
	db = sqlite3.connect("../interface_large.db")
	return db

def connect_to_raw_interface():
	db = sqlite3.connect("../large_interface_insecure.db")
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
		
		lmap[group] = {}
		for response in responses:
			lmap[group][response] = lid
			c.execute("""INSERT INTO responses VALUES(?,?,?,?);""", (gid, lid, group, response))
			lid += 1
		#print
	
	return [gmap, lmap]

def main():
	q1 = ["< 3 months", "3 to 6 months", "6 months to a year", "1 to 2 years", "2 to 3 years", "3 to 5 years", "> 5 years"]
	# Primary browser
	q4 = ["Only Firefox", "Firefox", "Chrome", "Safari", "Opera", "Internet Explorer"]
	# gender
	q5 = ["Male", "Female"]
	#q5 = ["Female", "Male"]
	# age
	q6 = ["Under 18", "18-25", "26-35", "36-45", "46-55", "Older than 55"]
	# time spent on web
	q7 = ["< 1 hr", "1-2 hrs", "2-4 hrs", "4-6 hrs", "6-8 hrs", "8-10 hrs", "> 10 hrs"]
	# how would you describe your experience level? scale 1-10
	q8 = range(0,11)
	
	os_stuff = ["Windows", "Mac", "Linux", "Other"]
	
	extensions = ["0", "1", "2-5", "> 5"]
	
	private_browsing = ["No", "Yes"]
	
	search_count = ["< 10 an hour", "10 - 100", "> 100"]
	
	context_menu = ["No", "Yes"]
	
	
	
	responses = {
		"Firefox usage": q1,
		"Primary browser":                 q4,
		"Gender":                          q5,
		"Age":                             q6,
		"Time on web":                     q7,
		"Experience Level":                q8,
		"OS":                              os_stuff,
		"Extensions":                      extensions,
		"Uses Private Browsing":           private_browsing,
		"Search Frequency":                search_count,
		"Uses Context Menus":              context_menu
	}
	
	srs = {
	1:"Firefox usage",
	4:"Primary browser",
	5:"Gender",
	6:"Age",
	7:"Time on web",
	8:"Experience Level"
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
	
	db3 = connect_to_raw_interface()
	c3 = db3.cursor()
	
	gmap, lmap = add_responses(responses, c)
	
	def os_converter(os_string):
		if "Windows" in os_string:
			os_string = "Windows"
		elif "Mac" in os_string:
			os_string = "Mac"
		elif "Linux" in os_string:
			os_string = "Linux"
		else:
			os_string = "Other"
		return os_string
	
	def extensions_converter(count):
		if count == 0:
			count = "0"
		elif count == 1:
			count = "1"
		elif count <= 5 and count >= 2:
			count = "2-5"
		else:
			count = "> 5"
		return count
	
	def pb_converter(count):
		if count > 0:
			count = "Yes"
		else: count = "No"
		return count
	
	def search_converter(count):
		if count < 10:
			count = "< 10 an hour"
		elif count >= 10 and count <= 100:
			count = "10 - 100"
		elif count > 100:
			count = "> 100"
		return count
	
	def context_converter(value):
		if value == True:
			value = "Yes"
		else:
			value = "No"
		return value
	
	def query_to_dict(q, c, k, converter=lambda x: x, cache_queryset = True, cache_final = True):
		m = {}
		s = shelve.open('shelve')
		if s.has_key(k) and cache_final == True and cache_queryset == True:
			m = s[k]
		else:
			print "No shelf for %s.  Going from scratch." % k
			if s.has_key(q) and cache_queryset == True:
				for (user_id, val) in s[q]:
					m[user_id] = lmap[k][converter(val)]
			else:
				print "No shelf for query \n\n %s \nGoing from scratch." % q
				c.execute(q)
				s[q] = c.fetchall()
				data = s[q]
				for (user_id, val) in data:
					m[user_id] = lmap[k][converter(val)]
			s[k] = m
		return m
	
	extensions_query = """SELECT user_id, COUNT(*)-1 FROM user_extensions GROUP BY user_id;"""
	pb_query = """SELECT user_id, CAST(count(*) AS REAL)/2 AS pb FROM events WHERE sub_item LIKE 'private%' GROUP BY user_id;"""
	search_query = """SELECT user_id, avg(td) AS avg_td FROM
		(SELECT 
			user_id,
			(COUNT(item = 'searchbar' OR (item = 'urlbar' AND sub_item = 'search term')) / CAST((max(timestamp)/1000 - min(timestamp)/1000) AS REAL)) * (60 * 60) AS td,
			session_id 
		FROM 
			events 
		GROUP BY 
			user_id, session_id
		HAVING td NOT NULL AND td < 600) AS search
		GROUP BY user_id;"""
		
	context_query = """SELECT user_id, COUNT(*) > 0 AS cnt FROM events
		WHERE sub_item LIKE 'context%'
		GROUP BY user_id;"""
	
	emap = query_to_dict(extensions_query, c3, "Extensions", converter = extensions_converter)
	pbmap = query_to_dict(pb_query, c3, "Uses Private Browsing", converter = pb_converter)
	searchmap = query_to_dict(search_query, c3, "Search Frequency", converter = search_converter, cache_final = False)
	contextmap = query_to_dict(context_query, c3, "Uses Context Menus", converter = context_converter)
	
	print "finished queries."
	
	for (qrow) in c2.execute(query1):
		user_id = qrow[0]
		
		spots = [lmap[srs[i]][response_map[i][int(qrow[i])]] for i in qs if qrow[i] != None]
		
		c3.execute("SELECT os FROM users WHERE id = ?;", [user_id])
		os_ = c3.fetchone()[0]
		os_ = lmap["OS"][os_converter(os_)]
		
		spots.append(os_)
		
		spots.append(emap[user_id])
		
		if user_id in pbmap:
			spots.append(pbmap[user_id])
		else: spots.append(lmap["Uses Private Browsing"]["No"])
		
		if user_id in searchmap:
			spots.append(searchmap[user_id])
		else: 
			spots.append(lmap["Search Frequency"]["< 10 an hour"])
		
		if user_id in contextmap: spots.append(contextmap[user_id])
		else: spots.append(lmap["Uses Context Menus"]["No"])
		
		# extensions
		
		if len(spots) > 2 and len(qrow) == 15:
			#print len(qrow)
			# add this to a user's dict.
			#print spots
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