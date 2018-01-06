import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options

options = Options() 
options.add_argument("--start-maximized") 

driver=webdriver.Chrome(chrome_options=options) 
driver.get("https://psns.cc.stonybrook.edu/psp/csprods/EMPLOYEE/CAMP/?cmd=login")
username = driver.find_element_by_id('userid')
password = driver.find_element_by_id('pwd')
username.send_keys("110875002")
password.send_keys("008009756")
login = driver.find_element_by_name('Submit')
login.click()


driver.get("https://psns.cc.stonybrook.edu/psc/csprods/EMPLOYEE/CAMP/c/PRJCS_MENU.PRJCS_SCHD_STRT.GBL?PORTALPARAM_PTCNAV=PRJCS_SCHD_STRT&EOPP.SCNode=CAMP&EOPP.SCPortal=EMPLOYEE&EOPP.SCName=ADMN_SOLAR_SYSTEM&EOPP.SCLabel=Enrollment&EOPP.SCFName=HCCC_ENROLLMENT&EOPP.SCSecondary=true&EOPP.SCPTcname=PT_PTPP_SCFNAV_BASEPAGE_SCR&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.SU_STUDENT_FOLDER.HCCC_ENROLLMENT.PRJCS_SCHD_STRT&IsFolder=false&PortalActualURL=https%3a%2f%2fpsns.cc.stonybrook.edu%2fpsc%2fcsprods%2fEMPLOYEE%2fCAMP%2fc%2fPRJCS_MENU.PRJCS_SCHD_STRT.GBL&PortalContentURL=https%3a%2f%2fpsns.cc.stonybrook.edu%2fpsc%2fcsprods%2fEMPLOYEE%2fCAMP%2fc%2fPRJCS_MENU.PRJCS_SCHD_STRT.GBL&PortalContentProvider=CAMP&PortalCRefLabel=Schedule%20Builder&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fpsns.cc.stonybrook.edu%2fpsp%2fcsprods%2f&PortalURI=https%3a%2f%2fpsns.cc.stonybrook.edu%2fpsc%2fcsprods%2f&PortalHostNode=CAMP&NoCrumbs=yes&PortalKeyStruct=yes")

open_builder = driver.find_element_by_id("PRJCS_DERIVED_PRJCS_LAUNCH_CS")
open_builder.click()

sleep(8)

if len(driver.window_handles) < 2:
	sleep(10)

while len(driver.window_handles) < 2:
	print "Waiting for next browser..."
	sleep(5)

driver.switch_to.window(driver.window_handles[1])

driver.get("https://stonybrook.collegescheduler.com/terms/Spring%202018/options")

sleep(5)

shopping_cart = driver.find_elements_by_class_name("shopping-cart")

def parse_shopping_cart(shopping_cart):

	shopping_cart_strings = []

	for item in shopping_cart:
		shopping_cart_strings.append(item.text)

	shopping_cart_strings = shopping_cart_strings[0].split('\n')
	shopping_cart_strings = shopping_cart_strings[2:]
	return shopping_cart_strings


def create_shopping_item(subject,setting):

	shopping_item = {
		"subject" : subject,
		"setting" : setting
	}

	return shopping_item

def parse_shopping_items(shopping_strings):

	shopping_items = []

	for index in range(len(shopping_strings)):

		if (index + 1) % 3 == 0:
			subject = shopping_strings[index-2][:7]
			setting = shopping_strings[index]
			shopping_items.append(create_shopping_item(subject,setting))

	return shopping_items

def find_correct_course(shopping_item):
	course = shopping_item['subject']
	xpath = '//*[strong= "'+ str(course) + '"]'
	course_name = driver.find_element_by_xpath(xpath)
	course_item = course_name.find_element_by_xpath("..")
	course_id = course_item.get_attribute("data-id")
	driver.get("https://stonybrook.collegescheduler.com/terms/Spring%202018/courses/" + str(course_id))




shopping_strings = parse_shopping_cart(shopping_cart)
shopping_items = parse_shopping_items(shopping_strings)

for item in shopping_items:
	print item['subject'], item['setting']

find_correct_course(shopping_items[1])













