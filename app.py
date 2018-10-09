# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import json
import datetime
from dateutil.parser import parse
ignore_subjects = [u'Personal and Family Finance', u'Orientation - High School Stud', u'Chinese Mandarin Course 2', u'HS Physical Education', u'State History Report']
today = datetime.datetime.today().date()
start_week = today - datetime.timedelta(today.weekday())
end_week = start_week + datetime.timedelta(6)
with open('data.json') as f:
     data = json.load(f)
for s in ignore_subjects:
    del data[s]
subjects = data.keys()
print(subjects)
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
    for a in assignments:
        dt = assignments[a]
        if not dt == 'X':
            date = parse(dt)
            if date.date() == today:
                done[subject]['day'] = done[subject]['day'] + 1
            if date.date() < end_week and date.date() > start_week:
                done[subject]['week'] = done[subject]['week'] + 1
    today_d.append(done[subject]['day'])
    week_d.append(done[subject]['week'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
     html.Div([
        html.Div([
            dcc.Graph(
                id='completion-level',
                figure={
                    'data': [
                        {'x': subjects, 'y': completion, 'type': 'bar', 'name': 'Completion'},
                    ],
                    'layout': {
                        'title': 'Class Completion Level'
                    }
                }
            )
            ], className="six columns"),

        html.Div([
    dcc.Graph(
        id='completed-today',
        figure={
            'data': [
                {'x': subjects, 'y': today_d, 'type': 'bar', 'name': 'Done Today'},
            ],
            'layout': {
                'title': 'Assignments Completed Today'
            }
        }
    )
            ], className="six columns"),
        html.Div([
   dcc.Graph(
            id='completed-this-week',
            figure={
                'data': [
                    {'x': subjects, 'y': week_d, 'type': 'bar', 'name': 'Done This Week'},
                ],
                'layout': {
                    'title': 'Assignments Completed This Week'
                }
            }
        )
            ], className="six columns"),
   ], className="row")
])

if __name__ == '__main__':
    app.run_server(debug=True, host='10.20.100.203')
