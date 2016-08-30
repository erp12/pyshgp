from __future__ import absolute_import, division, print_function, unicode_literals

import math
import datetime

import plotly
import plotly.graph_objs as go


timings = { "evaluation":[],
            "genetics":[]}
total_errors_in_evalutaion_order = []


def plot_piano_roll():
	plotly.offline.plot({
    	"data": [go.Scatter(x=range(len(total_errors_in_evalutaion_order)),
    					 	y=total_errors_in_evalutaion_order,
    						mode = 'markers',
    						marker = dict(
						        color = 'rgba(85, 109, 255, .3)')
    						)],
    	"layout": go.Layout(xaxis= dict(title = 'Evaluation'),
    						yaxis = dict(title = 'Total Error',
    							         type='log'))
    })

def log_timings(stage, start, end):
    start = (start-datetime.datetime(1970,1,1)).total_seconds()
    end = (end-datetime.datetime(1970,1,1)).total_seconds()
    timings[stage].append(end - start)

def print_timings():
    print("Timings:")
    print("Evaluation Times (each gen):", list(map(lambda x: round(x, 3), timings['evaluation'])))
    print("Selection/Variations Times (each gen):", list(map(lambda x: round(x, 3), timings['genetics'])))
    print("Average Evaluation Timing of Generation:", round(sum(timings['evaluation']) / float(len(timings['evaluation'])), 3))
    print("Average Selection/Variations Timing of Generation:", round(sum(timings['genetics']) / float(len(timings['genetics'])), 3))