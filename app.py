# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import json
import datetime
import arrow
import os.path, time
from dateutil.parser import parse
ignore_subjects = [u'WordBuild Elements 1',u'Personal and Family Finance', u'Orientation - High School Stud', u'Chinese Mandarin Course 2', u'HS Physical Education', u'State History Report']
today = datetime.datetime.today().date()
start_week = today - datetime.timedelta(today.weekday())
end_week = start_week + datetime.timedelta(6)
file = 'data.json'
last_modified = parse(time.ctime(os.path.getmtime(file)))
with open(file) as f:
     data = json.load(f)
for s in ignore_subjects:
    del data[s]
subjects = data.keys()
grades = []
completion = []
done = {}
today_d = []
week_d = []
for subject in subjects:
    s = data[subject]
    done[subject]={}
    done[subject]['week'] = 0
    done[subject]['day'] = 0
    assignments = s['assignments']
    try:
        grades.append(int(data[subject]['grade']))
    except ValueError:
        grades.append(0)
    try:
        completion.append(int(data[subject]['percentage'].strip('%')))
    except ValueError:
        completion.append(0)
    latest_date = parse('1/1/2000')
    for a in assignments:
        dt = assignments[a]
        if not dt == 'X':
            date = parse(dt)
            if date.date() == today:
                done[subject]['day'] = done[subject]['day'] + 1
            if date.date() < end_week and date.date() > start_week:
                done[subject]['week'] = done[subject]['week'] + 1
            if date > latest_date:
                latest_date = date
    today_d.append(done[subject]['day'])
    week_d.append(done[subject]['week'])
    s['latest_date'] = latest_date

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def generate_subject_widget(subject):
    s = data[subject]
    latest_date_a = arrow.get(s['latest_date'])
    return html.Div(children=
        [
            html.H4(
                subject
            ),
            html.P(
                'Last activity: {}'.format(latest_date_a.format('ddd, MMM D'))),
            html.P(latest_date_a.shift(days=+1).humanize(), className="humanized_date"),
            html.H5(
                s['grade'] + '%'
            ),
            html.H5(
                'Today: {}'.format(done[subject]['day'])
            ),
            html.H5(
                'Week: {}'.format(done[subject]['week'])
            )
        ], className="two columns")

def grade_widgets():
    div = []
    print('Getting subject widgets')
    for subject in subjects:
        div.append(generate_subject_widget(subject))
    return div

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.css.append_css({"external_url": 'https://fonts.googleapis.com/css?family=Roboto'})
app.layout = html.Div(children=
     [
         html.Div(children=[
             html.H1("Chloe's School Year 2018-2019"),
             html.H3('Last Updated: {}'.format(arrow.get(last_modified).humanize()))
         ]),
         html.Div(children=grade_widgets())
     ],
     className="row"
)

if __name__ == '__main__':
    app.run_server(debug=True, host='10.20.100.203')
