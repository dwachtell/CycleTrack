import plotly
import plotly.express as px
import json
from . import converters

def generate(cycle_data):
    '''Returns JSON for plotly dot graph of the application cycle.'''
    # Melt data
    melted = cycle_data.melt(id_vars=cycle_data.columns[0], value_vars=cycle_data.columns[1:], var_name='Actions', value_name='date')
    # Generate scatterplot
    fig = px.scatter(melted, x='date', y='name', color='Actions',
                     labels={
                         'date': 'Date',
                         'name':''
                     },
                     title="Application Cycle",
                     height=len(melted['name'].unique())*20) # Adjust height based on number of schools
    # Update names of traces to make more readable
    fig.for_each_trace(lambda t: t.update(name=converters.action_names[t.name],
                                          legendgroup=converters.action_names[t.name],
                                          hovertemplate=t.hovertemplate.replace(t.name, converters.action_names[t.name])
                                          )
                       )
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    # Generate JSON for plotting
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON