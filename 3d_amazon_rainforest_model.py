import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Define Constants
saturation_rate = 0.6  # assumed growth rate
die_rate = 0.05  # assumed forest die-off rate
aridities = list(np.linspace(0.14, 1.57, 100))

def c_crit(aridity):
    return 0.7 * aridity - 0.1

# Equilibrium forest state
def forest_state(die_rate=die_rate, saturation_rate=saturation_rate):
    return 1 - die_rate / saturation_rate

def next_step(cover, aridity, die_rate=die_rate, saturation_rate=saturation_rate):
    if cover <= c_crit(aridity):
        dcdt = -die_rate * cover
    else:
        dcdt = saturation_rate * (1 - cover) * cover - die_rate * cover
    return cover + dcdt

def k_steps(cover, aridity, k, die_rate=die_rate, saturation_rate=saturation_rate):
    ret = [cover]
    while len(ret) < k:
        ret.append(next_step(ret[-1], aridity, die_rate, saturation_rate))
    return ret

def return_time(initial_cover, aridity, max_steps=1000, eps=1e-6):
    cover = initial_cover
    steps = 0
    while steps < max_steps:
        if cover <= c_crit(aridity):
            return 0, -10

        if abs(cover - forest_state()) <= eps:
            return forest_state(), steps

        else: 
            cover = next_step(cover, aridity)
            steps += 1

    if steps == max_steps:
        return None, float('inf')

    return cover, steps

def char_return_time(equilibrium='F', saturation_rate=saturation_rate, die_rate=die_rate):
  if equilibrium == 'F':
      char_return_time = 1/(saturation_rate - die_rate)
      return char_return_time
  if equilibrium == 'S':
      char_return_time = 1/die_rate
      return char_return_time

def create_cover_time_aridities_figure(c0):
    time_steps = 50
    X, Y = np.meshgrid(np.linspace(0, 1, time_steps), aridities)
    Z = np.array([k_steps(c0, a, time_steps) for a in aridities])

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
    fig.update_layout(
        title=f'Vegetation Cover over Time and Aridity for C_0={c0}',
        scene=dict(
            xaxis_title='Time',
            yaxis_title='Aridity',
            zaxis_title='Vegetation Cover'
        ),
        autosize=True,
        width=700, height=700,
        margin=dict(l=65, r=50, b=65, t=90)
    )
    return fig

def create_return_time_figure(aridities, initial_values, eps=1e-6):
    X, Y = np.meshgrid(initial_values, aridities)
    Z = np.array([initial_values] * len(aridities))

    for ai, a in enumerate(aridities):
        for di, d in enumerate(initial_values):
            Z[ai][di] = return_time(d, a, eps=eps)[1]

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
    fig.update_layout(
        title='Global Return Time / Time Steps to Forest State',
        scene=dict(
            xaxis_title='Initial Tree Coverage',
            yaxis_title='Aridity',
            zaxis_title='Time'
        ),
        autosize=True,
        width=700, height=700,
        margin=dict(l=65, r=50, b=65, t=90)
    )
    return fig

def create_char_return_time_figure(equilibrium, saturation_rates, die_rates):
    X, Y = np.meshgrid(saturation_rates, die_rates)
    Z = np.zeros_like(X)

    for ri, r in enumerate(saturation_rates):
        for xi, x in enumerate(die_rates):
            Z[xi, ri] = char_return_time(equilibrium, r, x)
    equilibrium_name = 'Forest State' if equilibrium == 'F' else 'Savanna State'
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
    fig.update_layout(
        title=f'Characteristic Return Time for {equilibrium_name}',
        scene=dict(
            xaxis_title='Saturation Rate',
            yaxis_title='Death Rate',
            zaxis_title='Characteristic Return Time'
        ),
        autosize=True,
        width=700, height=700,
        margin=dict(l=65, r=50, b=65, t=90)
    )
    return fig

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    dcc.Slider(
        id='c0-slider',
        min=0,
        max=1,
        step=0.01,
        value=0.81,
        marks={i / 10: str(i / 10) for i in range(11)},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    dcc.Graph(id='3d-plot'),
    html.Br(),
    dcc.Graph(id='return-time-plot'),
    html.Br(),
    dcc.Graph(id='char-return-time-plot-forest'),
    html.Br(),
    dcc.Graph(id='char-return-time-plot-savanna')
])

@app.callback(
    Output('3d-plot', 'figure'),
    Input('c0-slider', 'value')
)
def update_figure(c0):
    return create_cover_time_aridities_figure(c0)

@app.callback(
    Output('return-time-plot', 'figure'),
    Input('c0-slider', 'value')
)
def update_return_time_figure(c0):
    initial_values = list(np.linspace(1e-6, 1, 1000))
    return create_return_time_figure(aridities, initial_values)

@app.callback(
    [Output('char-return-time-plot-forest', 'figure'),
     Output('char-return-time-plot-savanna', 'figure')],
    Input('c0-slider', 'value')
)
def update_char_return_time_figure(c0):
    saturation_rates = list(np.linspace(0.3, 0.7, 100))
    die_rates = list(np.linspace(0.01, 0.2, 100))
    fig_forest = create_char_return_time_figure('F', saturation_rates, die_rates)
    fig_savanna = create_char_return_time_figure('S', saturation_rates, die_rates)
    return fig_forest, fig_savanna

if __name__ == '__main__':
    app.run_server(debug=True)