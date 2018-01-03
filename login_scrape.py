import re
from robobrowser import RoboBrowser
from blackboard_credentials import username, password

# Browse to Genius
browser = RoboBrowser(history=True)
browser.open('https://blackboard.stonybrook.edu/webapps/login/')
print browser
form = browser.get_forms()[1]
form
form['user_id'].value = username
form['password'].value = password
browser.submit_form(form)

browser.open("https://blackboard.stonybrook.edu/webapps/bb-social-learning-bb_bb60/execute/mybb?cmd=display&toolId=MyGradesOnMyBb_____MyGradesTool")
src = browser.select("#iframe_wrap")

browser.open("https://blackboard.stonybrook.edu/webapps/bb-mygrades-bb_bb60/myGrades?course_id=_1131150_1&stream_name=mygrades")
grade_html =  str(browser.select(".grade"))


pattern = re.compile('\"0\">\d+\.\d\d+')

grades = re.findall(pattern, grade_html)
grades = list(set(grades))

for grade in range(len(grades)):
	grade_value = grades[grade][4:]
	grades[grade] = float(grade_value)

print grades
