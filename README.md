# WaitlistAlert
Utilizes Selenium library and Twilio API to send a text alert when a desired SB class has seats available

# Getting Set Up

Create a credentials.py file in same location as WaitlistAlert.py </ br>
Pull all pertinent information in there: </ br>
Solar username --> username </ br>
Solar password --> password </ br>
Twilio account SID --> client_id </ br>
Twilio Auth Token --> api_key</ br>
Phone Number --> my_number</ br>
Twilio Number --> twilio_number</ br>

# Installing Necessary Libraries

pip install virtualenv</ br>
virtualenv waitlistalert</ br>

if on Windows:
  waitlistalert\Scripts\activate.bat

else:
  source waitlistalert/bin/activate
  
pip install selenium</ br>
pip install chromebrowser</ br>
pip install twilio >=6.0.0</ br>

# Setting up Solar and Schedule Builder

add any wanted class to shopping cart in solar </ br>
in schedule builder, make sure to change course status to "Open & Full" </ br>
add the desired classes to the courses section by using the add course button </ br>

run script </ br>
