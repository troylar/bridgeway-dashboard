# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import json
import datetime
from datetime import date, timedelta
import arrow
import os.path
import time
from dateutil.parser import parse
import re
import pandas as pd

ignore_subjects = [u'WordBuild Elements 1',
                   u'Personal and Family Finance',
                   u'Orientation - High School Stud',
                   u'Chinese Mandarin Course 2',
                   u'HS Physical Education',
                   u'State History Report']
today = date.today()
offset = (today.weekday() - 3) % 7
start_week = today - timedelta(days=offset)
end_week = start_week + datetime.timedelta(6)
file = 'data.json'
last_modified = arrow.get(parse(time.ctime(os.path.getmtime(file)))).replace(tzinfo='local')

with open(file) as f:
    data = json.load(f)
for s in ignore_subjects:
    if s in data:
        del data[s]
subjects = data.keys()
grades = []
completion = []
done = {}
today_d = []
week_d = []
total_plus_b = 0
total_units_this_week = 0
total_units_today = 0
data_frame = {}

for subject in subjects:
    s = data[subject]
    data_frame[subject] = []
    done[subject] = {}
    done[subject]['week'] = 0
    done[subject]['day'] = 0
    assignments = s['assignments']
    data_frame[subject].append(subject)
    try:
        grade = int(data[subject]['grade'])
        if grade >= 80:
            total_plus_b = total_plus_b + 1
        grades.append(grade)
        data_frame[subject].append(grade)
    except ValueError:
        grades.append(0)

    try:
        percent = int(data[subject]['percentage'].strip('%'))
        completion.append(percent)
    except ValueError:
        completion.append(0)
        data_frame[subject].append(0)
    latest_date = parse('1/1/2000')
    latest_unit = 0
    highest_unit = 0
    total_units = 0
    completed_units = {}
    s['units_this_week'] = 0
    s['units_today'] = 0
    unit_done_dates = {}
    for a in assignments:
        m = re.match('^([0-9]+)\.([0-9]+)', a)
        if not m:
            continue
        unit = m.group(1)
        if unit not in completion:
            completed_units[unit] = True
        dt = assignments[a]
        unit_complete = True
        assignment_complete = False
        if not dt == 'X':
            assignment_complete = True
            date = parse(dt)
            if date.date() == today:
                done[subject]['day'] = done[subject]['day'] + 1
            if date.date() < end_week and date.date() > start_week:
                done[subject]['week'] = done[subject]['week'] + 1
            if date > latest_date:
                latest_date = date
            if unit not in unit_done_dates:
                unit_done_dates[unit] = date.date()
            else:
                if date.date() > unit_done_dates[unit]:
                    unit_done_dates[unit] = date.date()

        completed_units[unit] = completed_units[unit] and assignment_complete
        if int(unit) > highest_unit:
            highest_unit = int(unit)

    today_d.append(done[subject]['day'])
    week_d.append(done[subject]['week'])
    s['latest_date'] = latest_date
    s['latest_unit'] = 0
    s['highest_unit'] = highest_unit
    for unit in completed_units:
        if completed_units[unit]:
            s['latest_unit'] = unit
            if unit_done_dates[unit] == today:
                total_units_today = total_units_today + 1
                s['units_today']= s['units_today'] + 1
            if unit_done_dates[unit] < end_week and unit_done_dates[unit] > start_week:
                s['units_this_week'] = s['units_this_week'] + 1
                total_units_this_week = total_units_this_week + 1
    s['completion_date'] = arrow.now().shift(weeks=+(highest_unit - int(s['latest_unit'])))
    data_frame[subject].append(arrow.get(latest_date).shift(hours=+1).humanize())
    data_frame[subject].append('{} of {} ({})'.format(s['latest_unit'], s['highest_unit'], s['percentage']))
    data_frame[subject].append('{}'.format(s['completion_date'].format('MMM D, YYYY')))
    data_frame[subject].append(done[subject]['day'])
    data_frame[subject].append(done[subject]['week'])
    data_frame[subject].append(s['units_today'])
    data_frame[subject].append(s['units_this_week'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def generate_table(data, max_rows=100):
    dataframe = pd.DataFrame.from_dict(data, orient='index',
				       columns=['Subject',
                                                'Grade',
                                                'Latest Activity',
                                                'Highest Unit',
                                                'Est Complete Date',
                                                'Items Done Today',
                                                'Items Done This Week',
                                                'Units Done Today',
                                                'Units Done This Week',
                                               ])
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


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
                '{} Completed'.format(s['percentage'])),
            html.H5(
                'Current Grade: {}'.format(s['grade'] + '%')),
            html.H5(
                'Assignments Done:'
            ),
            html.H6(
                'Today/This Week: {}/{}'.format(done[subject]['day'], done[subject]['week'])
            ),
            html.H5(
                'Units Done:'
            ),
            html.H6(
                'Today/This Week: {}/{}'.format(s['units_today'], s['units_this_week'])
            ),
             html.H5(
                'Latest Unit: {} of {}'.format(s['latest_unit'], s['highest_unit'])
            ),
            html.H5(
                'Est Completion: {}'.format(s['completion_date'].format('MMM D, YYYY'))
            ),
        ], className="four columns")


def grade_widgets():
    div = []
    print('Getting subject widgets')
    for subject in subjects:
        div.append(generate_subject_widget(subject))
    return div

def render_layout():
    return html.Div(children=
	     [
		 html.Div(children=[
		     html.H4("Chloe's School Year 2018-2019"),
		     html.H6('Last Updated: {}'.format(arrow.get(last_modified).humanize())),
		     html.H5('Week: {} - {}'.format(arrow.get(start_week).format('ddd, MMM D'), arrow.get(end_week).format('ddd, MMM D'))),
		     html.H5('Total Units Done Today: {}'.format(total_units_today)),
		     html.H5('Total Units Done This Week: {} of 7'.format(total_units_this_week)),
		     html.H5('Required B\'s: {} of {}'.format(total_plus_b, len(subjects)))
		 ]),
		 html.Div(children=generate_table(data_frame))
	     ],
	     className="row"
	)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.css.append_css({"external_url": 'https://fonts.googleapis.com/css?family=Roboto'})
app.layout = render_layout
server = app.server
if __name__ == '__main__':
    app.run_server(debug=True, host='10.20.5.50', port=8050, extra_files=['./data.json'])
