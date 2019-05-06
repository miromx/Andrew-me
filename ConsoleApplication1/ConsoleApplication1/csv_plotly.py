import pandas as pd
import plotly
import plotly.graph_objs as go
import numpy as np

dn = pd.Series(["время","скорость","угол_траектории","высота","угол_тангажа","угловая_скорость_тангажа"])
df = pd.read_csv('rezultatiP1_10s_pikir.csv', names=dn)
df = df.convert_objects(convert_numeric=True)

xdata = df['время']

trace1 = go.Scatter(
    x=xdata,
    y=df['скорость'],
    mode='lines+markers',
    name='скорость'
)

trace2 = go.Scatter(
    x=xdata,
    y=df['угол_траектории'],
    mode='lines+markers',
    name='угол_траектории'
)

trace3 = go.Scatter(
    x=xdata,
    y=df['высота'],
    mode='lines+markers',
    name='высота'
)

trace4 = go.Scatter(
    x=xdata,
    y=df['угол_тангажа'],
    mode='lines+markers',
    name='угол_тангажа'
)

trace5 = go.Scatter(
    x=xdata,
    y=df['угловая_скорость_тангажа'],
    mode='lines+markers',
    name='угловая_скорость_тангажа'
)


data = [trace1,trace2,trace3,trace4,trace5]

layout = go.Layout(
        legend=dict(
                orientation="h",
                traceorder='normal',
                bgcolor='white',
                bordercolor='black',
                borderwidth=0.5
        ),
        title='Графики',
        showlegend=True,
        xaxis=dict(
            showgrid=True,
            mirror='ticks',
            title='X',
            ticks='',
            automargin=True,
            gridcolor='grey',
            gridwidth=0.5,
            zerolinecolor='black',
            zerolinewidth=0.25,
            linecolor='black',
            linewidth=0.5),
        yaxis=dict(
            showgrid=True,
            mirror='ticks',
            title='Y',
            ticks='',
            automargin=True,
            gridcolor='grey',
            gridwidth=0.5,
            zerolinecolor='black',
            zerolinewidth=0.25,
            linecolor='black',
            linewidth=0.5),
        width=900,
        height=700,
        margin=dict(
            l=80,
            r=50,
            b=50,
            t=30)
)
config = {
    'linkText': "a&m",
    'scrollZoom': True,
    'displayModeBar': True,
    'editable': True
}

plotly.offline.plot(dict(data=data, layout=layout), config=config, filename='simple-plots.html', auto_open=True)
