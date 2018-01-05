import re
from robobrowser import RoboBrowser
from blackboard_credentials import username, password
import time


# goes to blackboard login page
browser = RoboBrowser(parser= "html.parser", history=True)
browser.open('https://blackboard.stonybrook.edu/webapps/login/')

# gets the appropiate login form and inputs login credentials
form = browser.get_forms()[1]
form
form['user_id'].value = username
form['password'].value = password
browser.submit_form(form)

# navigate to grade tab
browser.open("https://blackboard.stonybrook.edu/webapps/bb-social-learning-bb_bb60/execute/mybb?cmd=display&toolId=MyGradesOnMyBb_____MyGradesTool")


# navigate to actual grade div 
browser.open("https://blackboard.stonybrook.edu/webapps/bb-mygrades-bb_bb60/myGrades?course_id=_1131150_1&stream_name=mygrades")

# get all info regarding grade 
grade_html =  str(browser.select(".grade"))


def get_score(grade_string):

	pattern = re.compile('\"0\">\d+\.\d\d+<\/span><')

	grades = re.findall(pattern, grade_string)

	for grade in range(len(grades)):
		grade_value = grades[grade][4:len(grades[grade])-8]
		grades[grade] = float(grade_value)

	return grades


def get_points_possible(possible_string):
	pattern = re.compile('\d+')
	points_possible = re.findall(pattern, possible_string)

	for points in range(len(points_possible)):

		points_possible[points] = float(points_possible[points])

	return points_possible


def get_grade_type(grade_type_string):
	pattern = re.compile('>\w+')
	grade_types = re.findall(pattern, grade_type_string)

	for i in range(len(grade_types)):

		grade_types[i] = grade_types[i][1:]

	return grade_types


scores = get_score(grade_html)
print "Scores: ", scores
possible_html = str(browser.select(".pointsPossible"))
points_possible = get_points_possible(possible_html)
print "Possible Points: " , points_possible
grade_type_string = str(browser.select(".itemCat"))
grade_types = get_grade_type(grade_type_string)
print "Grade Types: ", grade_types

browser.open("https://blackboard.stonybrook.edu/webapps/bb-mygrades-bb_bb60/myGrades?course_id=_1131160_1&stream_name=mygrades")
grade_html = str(browser.select(".grade"))
scores = get_score(grade_html)
print "Scores: ", scores
possible_html = str(browser.select(".pointsPossible"))
points_possible = get_points_possible(possible_html)
print "Possible Points: " , points_possible

browser.open("https://blackboard.stonybrook.edu/webapps/bb-mygrades-bb_bb60/myGrades?course_id=_1133163_1&stream_name=mygrades")
grade_html = str(browser.select(".grade"))
scores = get_score(grade_html)
print "Scores: ", scores
possible_html = str(browser.select(".pointsPossible"))
points_possible = get_points_possible(possible_html)
print "Possible Points: " , points_possible







