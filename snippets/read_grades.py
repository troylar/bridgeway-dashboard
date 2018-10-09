import json
import arrow
import datetime
from dateutil.parser import parse
today = datetime.datetime.today().date()
start_week = today - datetime.timedelta(today.weekday())
end_week = start_week + datetime.timedelta(6)
print(start_week)
print(end_week)
with open('data.json') as f:
    data = json.load(f)
for subject in data:
    d = data[subject]
    for a in d['assignments']:
        dt = d['assignments'][a]
        if not dt == 'X':
            date = parse(dt)
            print(date.date() == today)
