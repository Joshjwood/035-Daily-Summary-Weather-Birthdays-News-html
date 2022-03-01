import pandas
import datetime as dt
def birthday_alert():
    now = dt.datetime.now()
    day = now.day
    month = now.month

    monthname = now.strftime("%B")

    its_your_birthday = ""
    with open("birthdays.csv") as birthday_data:
        birthdays = pandas.read_csv(birthday_data)
        birthdays = birthdays.to_dict()
        its_your_birthday = "<br>"
        for index in range(0, len(birthdays["name"])):
            if int(month) == int(birthdays["month"][index]) and int(day) == int(birthdays["day"][index]):
                its_your_birthday += f"<br>It's <strong>{birthdays['name'][index]}</strong>'s birthday today."
        if len(its_your_birthday) < 5:
            its_your_birthday = ""


        monthly_birthdays = f"<br><strong>Birthdays in {monthname}:</strong><br>"
        for index in range(0, len(birthdays["name"])):
            if int(month) == int(birthdays["month"][index]) and int(day) <= int(birthdays["day"][index]):
                monthly_birthdays += f"It\'s {birthdays['name'][index]}\'s birthday on {monthname} {int(birthdays['day'][index])}.<br>"

        birthday_text = its_your_birthday + "<br>" + monthly_birthdays

        return birthday_text
