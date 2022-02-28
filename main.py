import smtplib
import time
from weather_alerts import tomorrow_weather, today_weather, get_weather_data
from news_reports import bbc_today, reuters_today, guardian_today, yesterday_top_3
from birthday_alert import birthday_alert
from privates import *
from email_css import *

my_email = MY_EMAIL
password = PASSWORD
my_main_email = MY_MAIN_EMAIL

weather_data = get_weather_data()
news_block = bbc_today() + reuters_today() + guardian_today() + yesterday_top_3()

#########Sending#########

message = email_css_start
message += today_weather(weather_data) + tomorrow_weather(weather_data) + "\n\n" + birthday_alert() + "\n\n" + news_block + f"\n \nThis email has been brought to you by Josh Wood's automation services, making janky shit work since several months ago.\n \n JWA: Fail upwards"
message += email_css_end

connection = smtplib.SMTP("smtp.gmail.com")
connection.starttls()
connection.login(user=my_email, password=password)
connection.sendmail(from_addr=my_email, to_addrs=my_main_email, msg=message.encode("utf-8"))
time.sleep(10)
connection.close()