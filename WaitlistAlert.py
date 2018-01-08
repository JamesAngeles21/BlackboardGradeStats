import re
import credentials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client


# navigate to solar site and login
def login_solar():

	driver.get("https://psns.cc.stonybrook.edu/psp/csprods/EMPLOYEE/CAMP/?cmd=login")
	username = driver.find_element_by_id('userid')		
	password = driver.find_element_by_id('pwd')
	username.send_keys(credentials.username)
	password.send_keys(credentials.password)
	login = driver.find_element_by_name('Submit')
	login.click() 



# open schedule builder, close previous tab, and switch focus to schedule builder main page

def open_schedule_builder():
	driver.get("https://psns.cc.stonybrook.edu/psc/csprods/EMPLOYEE/CAMP/c/PRJCS_MENU.PRJCS_SCHD_STRT.GBL?PORTALPARAM_PTCNAV=PRJCS_SCHD_STRT&EOPP.SCNode=CAMP&EOPP.SCPortal=EMPLOYEE&EOPP.SCName=ADMN_SOLAR_SYSTEM&EOPP.SCLabel=Enrollment&EOPP.SCFName=HCCC_ENROLLMENT&EOPP.SCSecondary=true&EOPP.SCPTcname=PT_PTPP_SCFNAV_BASEPAGE_SCR&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.SU_STUDENT_FOLDER.HCCC_ENROLLMENT.PRJCS_SCHD_STRT&IsFolder=false&PortalActualURL=https%3a%2f%2fpsns.cc.stonybrook.edu%2fpsc%2fcsprods%2fEMPLOYEE%2fCAMP%2fc%2fPRJCS_MENU.PRJCS_SCHD_STRT.GBL&PortalContentURL=https%3a%2f%2fpsns.cc.stonybrook.edu%2fpsc%2fcsprods%2fEMPLOYEE%2fCAMP%2fc%2fPRJCS_MENU.PRJCS_SCHD_STRT.GBL&PortalContentProvider=CAMP&PortalCRefLabel=Schedule%20Builder&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fpsns.cc.stonybrook.edu%2fpsp%2fcsprods%2f&PortalURI=https%3a%2f%2fpsns.cc.stonybrook.edu%2fpsc%2fcsprods%2f&PortalHostNode=CAMP&NoCrumbs=yes&PortalKeyStruct=yes")
	open_builder = driver.find_element_by_id("PRJCS_DERIVED_PRJCS_LAUNCH_CS")
	open_builder.click()

	sleep(8)

	if len(driver.window_handles) < 2:			# accounts for page loading
		sleep(10)

	while len(driver.window_handles) < 2:
		print "Waiting for next browser..."
		sleep(5)

	schedule_builder_window = driver.window_handles[1]

	driver.switch_to.window(driver.window_handles[1])
	driver.switch_to.window(driver.window_handles[0])
	driver.close()

	driver.switch_to.window(schedule_builder_window)
	driver.get("https://stonybrook.collegescheduler.com/terms/Spring%202018/options")


# stores only necessary shopping cart information into array (subject, setting, professor)

def parse_shopping_cart(shopping_cart):

	shopping_cart_strings = []

	for item in shopping_cart:
		shopping_cart_strings.append(item.text)

	shopping_cart_strings = shopping_cart_strings[0].split('\n')
	shopping_cart_strings = shopping_cart_strings[2:]
	return shopping_cart_strings


def create_shopping_item(subject,setting, professor):

	shopping_item = {
		"subject" : subject,
		"setting" : setting,
		"professor": professor
	}

	return shopping_item

# creates shopping cart objects/dict from array of strings
# every 3 elements represent one shopping cart object
def parse_shopping_items(shopping_strings):

	shopping_items = []

	for index in range(len(shopping_strings)):

		if (index + 1) % 3 == 0:
			subject = shopping_strings[index-2][:7]
			setting = shopping_strings[index]
			professor = shopping_strings[index - 1]
			shopping_items.append(create_shopping_item(subject,setting, professor))

	return shopping_items

# uses xpath to find the appropiate course and navigates to all of its sections	

def find_correct_course(shopping_item):
	course = shopping_item['subject']
	xpath = '//*[strong= "'+ str(course) + '"]'
	course_name = driver.find_element_by_xpath(xpath)
	course_item = course_name.find_element_by_xpath("..")
	course_id = course_item.get_attribute("data-id")
	driver.get("https://stonybrook.collegescheduler.com/terms/Spring%202018/courses/" + str(course_id))

# puts all of course characteristics (seats available, section number, etc) into one array

def parse_course_characteristics():
	
	characteristics = driver.find_elements_by_class_name("row-label")

	parsed_characteristics = []

	for characteristic in characteristics:
		if str(characteristic.text) != '':
			parsed_characteristics.append(characteristic.text)


	return parsed_characteristics


def create_course_section(seats, setting, section, professor):

	course_section = {

		"seats": seats,
		"setting": setting,
		"section": section,
		"professor": professor
	}

	return course_section



# separates elements in array into separate section objects
def parse_sections(course_sections):

	parsed_course_sections = []

	for index in range(len(course_sections)):

		if (index + 1) % 7 == 0 and index != 0:
			seats = course_sections[index - 4]
			setting = course_sections[index - 2]
			section = course_sections[index - 6]
			professor = course_sections[index - 3]
			course_section = create_course_section(seats,setting,section,professor)
			parsed_course_sections.append(course_section)

	return parsed_course_sections


def get_section(setting, professor):

	sections = parse_sections(parse_course_characteristics())		# puts all section objects into an array


	# finds appropiate section based off of where/when the class takes place and who is teaching the class
	for section in sections:
		if section['setting'] == setting and section['professor'] == professor:
			return section

	return None


# sends text message, notifying person that the class is available
def send_available(section, subject):

	message =  subject + " (S" + str(section['section']) +  ") taught by " + str(section['professor']) + " has " + section['seats'] + " seats left!"


	client = Client(credentials.client_id, credentials.api_key)

	client.messages.create(to=credentials.my_number,from_=credentials.twilio_number, body= message)


# sends text message, notifying person that class is unavailable
def send_not_available(section, subject):

	message = subject +  " (S" + str(section['section']) +  ") taught by " + str(section['professor']) +  " just became unavailable!"

	client = Client(credentials.client_id, credentials.api_key)

	client.messages.create(to=credentials.my_number,from_=credentials.twilio_number, body= message)


# finds first section in section array, used to see if the number of seats has changed in the section
def find_first_section(sections, section):

	for course_section in sections:
		if course_section['setting'] == section['setting'] and course_section['professor'] == section['professor']:
			return course_section

	return None



# goes through all the shopping items in cart and constantly checks if each class section in the cart is available or not 
def check_courses(shopping_items):
	available = []
	unavailable = []
	sections = []
	count = 0



	while True:

		for shopping_item in shopping_items:
			find_correct_course(shopping_item)
			sleep(5)							# accounts for page loading

			section = get_section(shopping_item['setting'], shopping_item['professor'])

			if count == 0:
				sections.append(section)		# if first iteration, puts section in section array (used to check for changes in seating, but is still available)

			# if the section has seats available and the section wasn't already available
			if int(section['seats']) > 0 and section not in available:
				send_available(section, shopping_item['subject'])	# send text message
				available.append(section)							# put in the known available array
				if section in unavailable:							# remove it from the unavailable array if there
					unavailable.remove(section)


			# if section has no more seats available and section wasn't already unavailable
			elif int(section['seats']) == 0 and section not in unavailable:
				send_not_available(section, shopping_item['subject'])
				unavailable.append(section)
				if section in available:
					available.remove(section)


			# if section has seats, but the number of seats available has changed since previous check
			elif int(section['seats']) > 0 and int(section['seats']) != int(find_first_section(sections, section)['seats']):
				send_available(section, shopping_item['subject'])
				find_first_section(sections, section)['seats'] = section['seats']		# set section seats to updated # of seats


			driver.execute_script("window.history.go(-1)")		# go back to schedule builder main page
			sleep(5)		# sleep to account for page loading

		count += 1 			# increase iteration count
		sleep(60)			# checks class availability every minute 
		open_schedule_builder()		# reopen schedule builder after all course sections are checked in order to check for updates
		sleep(5)		# account for page loading


options = Options() 
options.add_argument("--start-maximized") 

driver= webdriver.Chrome(chrome_options=options) 

login_solar()
open_schedule_builder()
sleep(5)

shopping_cart = driver.find_elements_by_class_name("shopping-cart")

shopping_strings = parse_shopping_cart(shopping_cart)
shopping_items = parse_shopping_items(shopping_strings)

check_courses(shopping_items)














