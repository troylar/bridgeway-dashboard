# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import json

with open('data.json') as f:
     data = json.load(f)
subjects = data.keys()
grades = []
completion = []
for subject in subjects:
    try:
        grades.append(int(data[subject]['grade']))
    except ValueError:
        grades.append(0)
    try:
        completion.append(int(data[subject]['percentage'].strip('%')))
    except ValueError:
        completion.append(0)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

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
])

if __name__ == '__main__':
    app.run_server(debug=True, host='10.20.100.203')
