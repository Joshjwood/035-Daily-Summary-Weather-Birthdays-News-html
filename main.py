import smtplib, ssl
import time
from weather_alerts import tomorrow_weather, today_weather, get_weather_data
from news_reports import bbc_today, reuters_today, guardian_today, yesterday_top_3
from birthday_alert import birthday_alert
from privates import *
from email_css import *

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

my_email = MY_EMAIL
password = PASSWORD
my_main_email = MY_MAIN_EMAIL

weather_data = get_weather_data()
news_block = bbc_today() + reuters_today() + guardian_today() + yesterday_top_3()

#########Sending#########

message = email_css_start
# The variable that glues it all together with some html formatting
message += today_weather(weather_data) + "<br>" + tomorrow_weather(weather_data) + f"{birthday_alert()}" + "<br><br>" + news_block + f"<br><br>This email has been brought to you by Josh Wood's automation services, making janky shit work since several months ago.\n \n JWA: Fail upwards"
message += email_css_end

text = message
html = message

message = MIMEMultipart("alternative")
message["Subject"] = f'Morning Report'
message["From"] = my_email
message["To"] = my_main_email

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

message.attach(part1)
message.attach(part2)

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(my_email, password)
    server.sendmail(
        my_email, my_main_email, message.as_string()
    )
print(f"Email(s) sorted.")