import math

import plotly
import plotly.graph_objs as go

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