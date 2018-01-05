import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep



driver = webdriver.Chrome()
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

sleep(5)

driver.switch_to.window(driver.window_handles[1])

driver.get("https://stonybrook.collegescheduler.com/terms/Spring%202018/options")
shopping_cart = driver.find_elements_by_class_name("section-item")
