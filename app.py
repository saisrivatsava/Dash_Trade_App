import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
from datetime import datetime, timedelta
import pandas as pd
import dash_reusable_components as drc


app = dash.Dash(__name__)
server = app.server

stock_list = pd.read_csv('resources/Stocks_List.csv',encoding = "ISO-8859-1")
stock_list.set_index('SecurityId', inplace=True)

options=[]
for stock in stock_list.index:
    mydict = {}
    mydict['label'] = stock_list.loc[stock]['SecurityName']+ ' '+ stock
    mydict['value'] = stock
    options.append(mydict)

def serve_layout():
    # App Layout
    return html.Div([
        # Banner display
        html.Div([
            html.H2(
                'TradeNimbus',
                id='title'
            )
        ],
            className="banner"
        ),
        # Body
        html.Div(className="container", children=[
            html.Div(className='row', children=[
                html.Div(className='five columns', children=[
                    drc.Card([
                        html.H4("Stocks Performence:")
                    ]),
                    drc.Card([
                        html.H4("Select Stocks:"),
                        drc.CustomDropdown(
                            id='my_ticker_symbol',
                            value=['TCS'],
                            options=options,
                            placeholder="Select Stocks",
                            multi = True
                        ),
                        html.Br(),
                        html.H4("Select Time Period:"),
                        drc.CustomDropdown(
                            id='my_date_dropdown',
                            options=[
                                {'label': ' Last week', 'value': 7},
                                {'label': ' One month', 'value': 30},
                                {'label': ' Three months', 'value': 90},
                                {'label': ' Six months', 'value': 180},
                                {'label': ' One year', 'value': 365},
                                {'label': ' Five years', 'value': 1825}
                            ],
                            value =180
                        ),
                        html.Button(
                            'Submit',
                            id='submit-button',
                            n_clicks=0,
                            style={'margin-right': '10px', 'margin-top': '5px'}
                        )
                    ])
                ]),

                html.Div(
                    className='seven columns',
                    style={'float': 'right'},
                    children=[
                        dcc.Graph(id='my_graph',
                        figure={'data':[
                        {'x':[1], 'y':[3]}
                        ], 'layout':{'title':'Graph is Loading..!!'}})
                        ])
                    ]
                )
            ])
        ])

app.layout = serve_layout

@app.callback(Output('my_graph', 'figure'),
                [Input('submit-button', 'n_clicks')],
                [State('my_ticker_symbol', 'value'),
                State('my_date_dropdown', 'value')
                ])
def update_graph(n_clicks, stock_ticker, past_value):
    present= datetime.today()
    past = present - timedelta(days=past_value)

    traces = []
    for stock in stock_ticker:
        df = web.DataReader("NSE:"+stock, "av-daily", past, present, access_key="NLT87NSAFSBF0MCB")
        traces.append({'x':df.index, 'y':df['close'], 'name':stock})
    fig = {'data':traces,
    'layout':{'title':stock}
    }
    return fig


if __name__ == '__main__':
    app.run_server()
