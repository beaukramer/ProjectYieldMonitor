
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_yield_monitor_plots(df):
    fig = go.Figure()

    for col in df:
        fig.add_trace(go.Box(y=df[col].values, name=df[col].name, notched=True, showlegend=False, selectedpoints=[-1],
                             yaxis='y2'))

    fig.add_trace(go.Scatter(x=list(df.columns), y=df.iloc[-1].values,
                             mode='markers', showlegend=False, marker=dict(size=12,
                                                                           line=dict(width=1, color='black'),
                                                                           color='black',
                                                                           symbol='diamond')))

    fig.update_layout(yaxis2=dict(
        matches='y',
        layer="above traces",
        overlaying="y",
    ),)

    return fig