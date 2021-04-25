import icalendar
import recurring_ical_events
import urllib.request
import imgkit
from datetime import date, timedelta, time, datetime
from collections import OrderedDict

TZ = datetime.now().astimezone().tzinfo


def fetch_calendars(filename, days):
    start_date = date.today()
    end_date = start_date + timedelta(days=days)

    with open(filename) as f:
        urls = f.read().splitlines()

    events = []
    for url in urls:
        # Downlaod ical
        ical_string = urllib.request.urlopen(url).read()
        calendar = icalendar.Calendar.from_ical(ical_string)
        calevents = recurring_ical_events.of(calendar).between(
            start_date, end_date)
        events.extend(calevents)
    events.sort(key=lambda event: dt(event["DTSTART"]))
    day_events = OrderedDict()
    for event in events:
        caldate = dt(event["DTSTART"]).date()
        # adjust end date of whole day event to same day
        dtend = (dt(event["DTEND"]) - timedelta(seconds=1)).date()
        while caldate <= dtend and caldate <= end_date:
            if caldate >= start_date:
                day_events.setdefault(caldate, list()).append(event)
            caldate += timedelta(days=1)
    return day_events


def tz():
    return TZ


def dt(entry):
    type = entry.params['value']
    if type == 'DATE-TIME':
        return entry.dt
    elif type == 'DATE':
        return datetime.combine(entry.dt, time(0, 0, tzinfo=tz()))
    else:
        return None
