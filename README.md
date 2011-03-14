PearsonBot
==========

PearsonBot is small data application that helps you visualize and test simple categorical associations.

Among the many flavors of data we collect at Mozilla, we often found ourselves wondering how to quickly analyze 
categorical data from surveys and other sources.


To pre-load it with fake data, run from the command line

	python; from contingency import init_db, test_data; init_db(); test_data()

To try the app, run

	python contingency.py

to run PearsonBot in a development setting, and you'll have a small example.

Table setup
-----------

The sqlite database setup we use is not the most elegant, but it works.  You will need two tables:

	CREATE TABLE contingency(lid1 INT, lid2 INT, count INT);
	CREATE TABLE responses(gid INT, lid INT, gname TEXT, lname TEXT);

`responses` is the table that contains all the labeling for the features.  The `gname` column is the group name, 
while the `lname` column is the label name.  For instance for the `os` group, we might have `mac`, `windows`, and `linux`.

The `gid` is a simple id for each group, while the `lid` is a simple (unique) id for each label.  For instance, a table might look like


	gid  lid  gname            lname
	__________________________________________
	2    2    Firefox usage    < 3 months
	2    3    Firefox usage    3 to 6 months
	2    4    Firefox usage    6 months to a year
	2    5    Firefox usage    1 to 2 years
	2    6    Firefox usage    2 to 3 years
	2    7    Firefox usage    3 to 5 years
	2    8    Firefox usage    > 5 years
	3    9    Gender           Male
	3    10   Gender           Female

`contingency` is a table that contains all the counts for the co-occurrences.  The table typically looks like this:

	lid1   lid2   count
	_________________________
	6      10     3042
	6      9      6353
	10     6      3042
	9      6      6353

Notice that both combinations of the label ids are in each table.  Seems unnecessary, but frankly the size of this database tends to be 
very small, so this kind of duplication isn't a burden.

We're hoping to write some simple scripts that will turn a csv of survey data (as well as a yaml file specifying the order of labels, if
that is necessary for userss) and outputs a simple db, ready to be used with the web app.