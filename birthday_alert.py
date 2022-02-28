import pandas
import datetime as dt
def birthday_alert():
    now = dt.datetime.now()
    day = now.day
    month = now.month
    its_your_birthday = ""
    with open("birthdays.csv") as birthday_data:
        birthdays = pandas.read_csv(birthday_data)
        birthdays = birthdays.to_dict()
        for index in range(0, len(birthdays["name"])):
            if int(month) == int(birthdays["month"][index]) and int(day) == int(birthdays["day"][index]):
                its_your_birthday = ""
                its_your_birthday += f"It's {birthdays['name'][index]}'s birthday."
        if len(its_your_birthday) < 1:
            its_your_birthday = "No known birthdays today."
        return its_your_birthday
