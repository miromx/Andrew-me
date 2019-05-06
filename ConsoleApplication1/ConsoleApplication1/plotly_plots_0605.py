import plotly
import plotly.graph_objs as go
import numpy as np

xdata = np.linspace(-10, 10, 101)
ydata = np.cos(xdata)

trace = go.Scatter(
    x=xdata,
    y=ydata,
    mode='lines+markers',
    name='cos'
)

trace1 = go.Scatter(
    x=xdata,
    y=np.sin(xdata),
    mode='lines+markers',
    name='sin'
)

data = [trace, trace1]

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
            title='Ось-Х',
            ticks='',
            gridcolor='grey',
            gridwidth=0.5,
            zerolinecolor='black',
            zerolinewidth=0.25,
            linecolor='black',
            linewidth=0.5),
        yaxis=dict(
            showgrid=True,
            mirror='ticks',
            title='Ось-У',
            ticks='',
            gridcolor='grey',
            gridwidth=0.5,
            zerolinecolor='black',
            zerolinewidth=0.25,
            linecolor='black',
            linewidth=0.5),
        width=800,
        height=600

)

config = {
    'linkText': "a&m",
    'scrollZoom': True,
    'displayModeBar': True,
    'editable': True
}

plotly.offline.plot(dict(data=data,layout=layout), config=config, filename='simple-plots.html', auto_open=True)
