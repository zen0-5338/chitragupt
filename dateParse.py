from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import tz


def dateParse(timeString):

    timeString = timeString.lower().strip().split()
    meridiemTimeInputFormat = "%I:%M %p"
    standardTimeInputFormat = "%H:%M"
    timeDisplayFormat = "%Y-%m-%d %A %I:%M %p"
    eventTime = None
    # timeDisplayFormat = "%c"

    try:
        if timeString[0] == "now":
            eventTime = datetime.strftime(datetime.now(), timeDisplayFormat)
            print(eventTime)

        elif timeString[0] == "after" or timeString[0] == "in":
            try:
                if timeString[2].lower().startswith("min"):
                    timeMin = float(timeString[1])
                    assert timeMin >= 0
                    eventTime = datetime.strftime(
                        datetime.now(tz=tz.time.timezone) + relativedelta(minutes=timeMin), timeDisplayFormat)
                    print(eventTime)

                elif timeString[2].startswith("h"):
                    timeHour = float(timeString[1])
                    if (len(timeString) > 3):# check if minutes mentioned
                        timeMin = float(timeString[3])
                    else:
                        timeMin = 0

                    assert timeHour >=0 and timeMin >=0
                    eventTime = datetime.strftime(
                        datetime.now() + relativedelta(hours=timeHour, minutes=timeMin), timeDisplayFormat
                    )
                    print(eventTime)

            except Exception as relativeTimeParsingException:
                print("relativeTimeParsingException , Type - {} : {}".format(
                    relativeTimeParsingException.__class__.__name__, relativeTimeParsingException))

        elif timeString[0] == "today":
            try:
                if len(timeString) > 3:                
                    eventTime = datetime.strptime(
                        timeString[2] + " " + timeString[3], meridiemTimeInputFormat)
                else:
                    eventTime = datetime.strptime(
                        timeString[2], standardTimeInputFormat)

                eventTime = datetime.strftime(
                    datetime.combine(date=datetime.today(), time=eventTime.time()) , timeDisplayFormat
                )
                #  eventTime = datetime.strftime(datetime.now() + relativedelta(hour=eventTime.hour,minute=eventTime.minute), timeDisplayFormat)
                print(eventTime)

            except Exception as todayException:
                print("todayException, Type - {} : {}".format(
                    todayException.__class__.__name__, todayException))
        
        elif timeString[0].startswith("tom"):
            try:
                if len(timeString) > 3:                
                    eventTime = datetime.strptime(
                        timeString[2] + " " + timeString[3], meridiemTimeInputFormat)
                else:
                    eventTime = datetime.strptime(
                        timeString[2], standardTimeInputFormat)
            
                    eventTime = datetime.strftime(
                        datetime.now() + relativedelta(days=1,hour=eventTime.hour,minute=eventTime.minute) , timeDisplayFormat
                    )
                    #  eventTime = datetime.strftime(datetime.now() + relativedelta(hour=eventTime.hour,minute=eventTime.minute), timeDisplayFormat)
                    print(eventTime)

            except Exception as tomorrowException:
                print("tomorrowException, Type - {} : {}".format(
                    tomorrowException.__class__.__name__, tomorrowException))

        elif timeString[0].find("day") != -1:
            dayDict = {"monday" : 0, "tuesday" : 1, "wednesday" : 2, "thursday":  3, "friday" : 4,"saturday" : 5,"sunday" : 6}
            try:
        
                day = dayDict[timeString[0]]
                if len(timeString) > 3:                
                    eventTime = datetime.strptime(
                        timeString[2] + " " + timeString[3], meridiemTimeInputFormat)
                else:
                    eventTime = datetime.strptime(
                        timeString[2], standardTimeInputFormat)
                
                eventTime = datetime.strftime(
                    datetime.now() + relativedelta(days=1,weekday=day,hour=eventTime.hour,minute=eventTime.minute), timeDisplayFormat
                )
                print(eventTime)

            except Exception as dayParsingException:
                print("dayParsingException, Type - {} : {} ".format(dayParsingException.__class__.__name__,dayParsingException))

    except Exception as dateParsingException:
        print("dateParsingException , Type - {} : {}".format(
            dateParsingException.__class__.__name__, dateParsingException))
    
    finally:
        return eventTime