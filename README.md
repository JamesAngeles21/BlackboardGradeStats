# WaitlistAlert
Utilizes Selenium library and Twilio API to send a text alert when a desired SB class has seats available

# Getting Set Up

Create a credentials.py file in same location as WaitlistAlert.py
Pull all pertinent information in there:
Solar username --> username
Solar password --> password
Twilio account SID --> client_id
Twilio Auth Token --> api_key
Phone Number --> my_number
Twilio Number --> twilio_number

# Installing Necessary Libraries

pip install virtualenv
virtualenv waitlistalert

if on Windows:
  waitlistalert\Scripts\activate.bat

else:
  source waitlistalert/bin/activate
  
pip install selenium
pip install chromebrowser
pip install twilio >=6.0.0

# Setting up Solar and Schedule Builder

add any wanted class to shopping cart in solar 
in schedule builder, make sure to change course status to "Open & Full"
add the desired classes to the courses section by using the add course button

run script
