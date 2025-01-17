import plotly
import plotly.graph_objects as go
import json
import textwrap
from . import converters

def generate(cycle_data,title,stats,color="default",map_scope="usa",custom_text=None):
    loc_df = converters.convert_map(cycle_data,color=color)
    fig = go.Figure()

    outcomes = list(loc_df["Best Outcome"].unique())
    for outcome in outcomes:
        outcome_df = loc_df.loc[loc_df["Best Outcome"] == outcome]
        fig.add_trace(go.Scattergeo(
            lon=outcome_df["long"],
            lat = outcome_df["lat"],
            text = outcome_df["school"]+"<br>Status: " + converters.action_names[outcome],
            hoverinfo="text",
            marker = dict(size = 10),
            marker_color=outcome_df["color"],
            name = converters.action_names[outcome]
        ))

    fig.update_layout(
        title=title,
        #title_x = 0.5,
        geo_scope = map_scope, width = 850,height = 400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    if map_scope == "north america":
        fig.update_geos(resolution=50,fitbounds="locations")

    fig.add_layout_image(
        dict(
        source="./static/images/CycleTrack_Plot_Watermark.png",
        xref="x domain",
        yref="y domain",
        x=1, y=1,
        sizex=0.2, sizey=0.2,
        xanchor="right", yanchor="bottom")
    )

    if custom_text:
        wrapped_text = textwrap.fill(custom_text,30).replace('\n', '<br />')

    if stats and custom_text:
        fig.add_annotation(
            dict(
            xanchor="left",
            yanchor="bottom",
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.02,
            y=0,
            text=f'Demographics<br>MCAT: {stats["mcat"]}<br>cGPA: {stats["cgpa"]}<br>sGPA: {stats["sgpa"]}'
                 f'<br>State: {stats["state"]}<br><br>{wrapped_text}',
            align="left"
            )
        )
    else:
        if stats:
            fig.add_annotation(
            dict(
            xanchor="left",
            yanchor="bottom",
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.02,
            y=0.2,
            text=f'Demographics<br>MCAT: {stats["mcat"]}<br>cGPA: {stats["cgpa"]}<br>sGPA: {stats["sgpa"]}'
                 f'<br>State: {stats["state"]}',
            align="left"
            )
        )
        if custom_text:
            fig.add_annotation(
                dict(
                xanchor="left",
                yanchor="bottom",
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1.02,
                y=0.2,
                text=f'{wrapped_text}',
                align="left"
                )
            )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
