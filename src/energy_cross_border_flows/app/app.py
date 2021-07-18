import pandas as pd
import plotly.express as px
import dash
from datetime import date
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import sys
import yaml

# ---------- Parameter of the app
app = dash.Dash(
    __name__,
    meta_tags=[{
        "name": "viewport",
        "content": "width=device-width, initial-scale=1"
    }],
)
app.title = "Cross-Border Flows"
app_color = {"graph_bg": "#F2F6FC", "graph_line": "#007ACE"}
server = app.server

# ---------- Import and clean data (importing csv into pandas)
# Load config file
configs = {}
with open('./config.yml', "r") as f:
    configs.update(yaml.load(f, Loader=yaml.FullLoader))

# Setup the per default variable and the scope
countries_a = list(configs['scope'].keys())
country_a = countries_a[0]
countries_b = configs['scope'][country_a].split(',')
country_b = countries_b[0]
date_value = "2021-06-30"

# Request the data display per default
query = f'http://{sys.argv[1]}:8000/date/{date_value}/country/{country_a}/country/{country_b}'
r = requests.get(
    query
)
pd_crossborder_flows = pd.DataFrame.from_dict(r.json())

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H4("Energy Cross-Border Flow",
                                className="app__header__title"),
                        html.P(
                            "This app is displaying the energetics from from The Netherlands and Germany and their surrounding countries.",
                            className="app__header__title--grey",
                        ),
                    ],
                    className="app__header__desc",
                )
            ],
            className="app__header",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="dropdown_a",
                            options=[{"label": x, "value": x}
                                     for x in countries_a],
                            value=country_a,
                            clearable=False,
                        ),
                    ],
                    style={
                        "width": "20%",
                        "height": "100px",

                    },
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="dropdown_b",
                            options=[{"label": x, "value": x}
                                     for x in countries_b],
                            value=country_b,
                            clearable=False,
                        ),
                    ],
                    style={
                        "width": "20%",
                        "height": "100px",

                    },
                ),
                html.Div(
                    [

                        dcc.DatePickerSingle(
                            id='my-date-picker-single',
                            min_date_allowed=date(2020, 8, 1),
                            max_date_allowed=date(2021, 7, 1),
                            initial_visible_month=date(2017, 8, 5),
                            date=date_value,
                            display_format='MMM Do, YY'
                        ),
                    ],
                    style={
                        "width": "20%",
                        "height": "100px",
                    },
                )
            ],
            style={
                'display': 'flex',
            },
        ),
        html.Div(
            [
                dcc.Graph(
                    id="bar-chart",
                ),
            ],
            className="app_graph"
        ),
    ],
    className="app__container",
    style={"backgroundColor": "#F2F6FC"}
)


@app.callback(
    Output('dropdown_b', 'options'),
    Input('dropdown_a', 'value')
)
def update_countries_b(country_a: str):
    """if we change country a, we need to update the list
    of country surrounding from country a. And then update
    the differents buton using the list.

    Args:
        country_a (str): The main counry to display

    Returns:
        Return the options to the dropdown from the list
    """
    countries_b = configs['scope'][country_a].split(',')
    options = [
        {"label": x, "value": x}
        for x in countries_b
    ]
    return options


@app.callback(
    Output('bar-chart', 'figure'),
    Input('my-date-picker-single', 'date'),
    Input("dropdown_a", "value"),
    Input("dropdown_b", "value")
)
def update_date_bar_chart(date_value: date, country_a: str, country_b: str):
    """Update the bar-chary depending on the countries requests by the user and
    the date

    Args:
        date_value (date): Day we want to display the information
        country_a (str): country A
        country_b (str): country B

    Returns:
        The plot Bar char.
    """
    requests_str = f'http://{sys.argv[1]}:8000/date/{date_value}/country/{country_a}/country/{country_b}'
    r = requests.get(
        requests_str
    )
    pd_crossborder_flows = pd.DataFrame.from_dict(r.json())

    # if not response from the api just display an empty Dataframe
    if len(pd_crossborder_flows) < 1:
        pd_crossborder_flows = pd.DataFrame()
        fig = px.bar(
            pd_crossborder_flows,
        )

    else:
        # Create label for exportation x Exportation
        pd_crossborder_flows['Type of flows'] = 'Importation'
        pd_crossborder_flows.loc[
            pd_crossborder_flows.country_code_to == country_b,
            'Type of flows'
        ] = 'Exportation'

        fig = px.bar(
            pd_crossborder_flows,
            x="flow_timestamp",
            y="capacity_mw",
            color="Type of flows",
            barmode="group",
            title=f"{date_value}, Energy's flow Between {country_a} and {country_b}"
        )

    # The Design x Colors of the Graph
    layout = dict(
        height=350,
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        xaxis={
            "title": "Date & Time",
            "showgrid": False,
            "showline": True,
            "fixedrange": True,
            "color": 'black'
        },
        yaxis={
            "title": "Capcity (mw)",
            "showgrid": True,
            "showline": False,
            "fixedrange": True,
            "color": 'black'
        },

        hovermode="closest",
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "xanchor": "center",
            "y": 1,
            "x": 0.5,

        },
    )
    fig.update_layout(layout)

    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
