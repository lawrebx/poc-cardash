from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

df_base = pd.read_csv(f"sample_data.csv")

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

dash_app = Dash(__name__)

app = dash_app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = df_base



dash_app.layout = html.Div(children=[
    html.H1(children='Welcome to Garbage Data LLC'),

    html.Div(children='''
        Garbage Data: Connecting garbage people to their garbage data.
    '''),

    html.Img(src='/assets/welcome-to-the-show-will-ferrell.gif'),

    html.Br(),

    html.Label('Dayparts'),
        dcc.Checklist(
                      ['Lunch', 'Dinner'],
                      ['Lunch', 'Dinner'],
                      id = 'daypart-checklist'
        ),

    html.Br(),

    html.Label('Wait Time'),
    dcc.Slider(
        id = "wait-time-input",
        min=df['hours'].min(),
        max=df['hours'].max(),
        marks={i: f'Hours {i}' if i == 1 else str(i) for i in range(df['hours'].min(), df['hours'].max())},
        value=df['hours'].max(),
        ),

    dcc.Graph(
        id = 'wait-graph-output'
    ),
    html.Div([
    html.H4(children='Service Record Data Table'),
    html.Table(id='wait-table-output')
])
])

@callback(
    Output(component_id='wait-graph-output', component_property='figure'),
    Output(component_id='wait-table-output', component_property='children'),
    Input(component_id='wait-time-input', component_property='value'),
    Input(component_id='daypart-checklist', component_property='value'),
)
def update_graph_wait(wait_input, daypart_input):

    df = df_base[df_base['hours']<=wait_input]

    df = df[df['time'].isin(daypart_input)]

    fig = px.box(df, x='location', y='gross_margin')

    fig.update_layout(transition_duration=500)

    tbl = generate_table(df)

    return fig, tbl

if __name__ == '__main__':
    app.run(debug=True)
