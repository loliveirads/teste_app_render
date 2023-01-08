#!pip install dash_bootstrap_components
#import dash_core_components as dcc
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
 
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

#from dash_bootstrap_templates import load_figure_template

df = pd.read_csv('supermarket_sales.csv')

df['Date'] = pd.to_datetime(df['Date'])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY],
               meta_tags=[{'name': 'viewport',
                           'content': 'width=device-width,initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])
server = app.server


app.layout = html.Div(children=[
    dbc.Row([
        dbc.Col([
            dbc.Card([
              html.H2("ASIMOV", style={"font-size": "25px", 'margin': '30px' }),
              html.Hr(),

              html.H5('Cidades',style={"font-family" : "Voltaire", "font-size": "20px", 'margin': '20px' }),
              dcc.Checklist(df['City'].unique(),
                            df['City'].unique(),# Aqui quer dizer que todos estarão marcados
                            id="check_city", # criando o id para depois chamarmos no callback)]
                            inputStyle={'margin-right' : '10px', 'margin-left' : '20px'}),

              html.H5('Variavel em análise:', style={"font-family" : "Voltaire", "font-size": "20px", 'margin': '20px','margin-top' : '30px'}),
              dcc.RadioItems(['gross income', 'Rating'], 
                              'gross income', # Aqui quer dizer que gross income já estará marcado
                              id='main_variable',
                              inputStyle={'margin-right' : '5px', 'margin-left' : '20px'}),
                ],style={'height': '90vh', 'margin': '10px', 'padding' : '1px'})
        ], sm=2),
        
        dbc.Col([
            dbc.Row([
                dbc.Col([dcc.Graph(id='city_fig')],sm=4),
                dbc.Col([dcc.Graph(id='gender_fig')],sm=4),
                dbc.Col([dcc.Graph(id='pay_fig')],sm=4)
            ]),
            dbc.Row([dcc.Graph(id='income_date_fig')]),
            dbc.Row([dcc.Graph(id='income_per_product_fig')])

            ],style={ 'margin-top': '10px'},sm=10)
        ])
    ]
)


#Callbacks

@app.callback([
                Output('city_fig', 'figure'),
                Output('pay_fig', 'figure'),
                Output('gender_fig', 'figure'),
                Output('income_per_product_fig', 'figure'),
                Output('income_date_fig', 'figure'),


            ],
              [
                Input('check_city', 'value'),
                Input('main_variable', 'value')
               
              ])
  
def render_graphs(cities, main_variable):
    
    operation = np.sum if main_variable == 'gross income' else np.mean
    
    df_filtered = df[df['City'].isin(cities)]
    
    df_city = df_filtered.groupby('City')[main_variable].apply(operation).to_frame().reset_index()
    df_gender = df_filtered.groupby(['Gender', 'City'])[main_variable].apply(operation).to_frame().reset_index()
    df_date = df_filtered.groupby('Date')[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby(['Payment', 'City'])[main_variable].apply(operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(['Product line', 'City'])[main_variable].apply(operation).to_frame().reset_index()

    
    fig_gender = px.bar(df_gender, y=main_variable, x='Gender',color='City',barmode='group')
    fig_city = px.bar(df_city, x='City', y=main_variable, color='City')
    fig_payment = px.bar(df_payment, x='Payment', y=main_variable, color='City', barmode='group')
    fig_product_income = px.bar(df_product_income, x=main_variable, y='Product line', color='City', orientation='h', barmode='group')
    fig_income_date = px.bar(df_date, x='Date', y=main_variable)

    fig_city.update_layout(margin=dict(l=0, r=0, t=20), height=200,template='plotly_dark')
    fig_payment.update_layout(margin=dict(l=0, r=0, t=20), height=200,template='plotly_dark')
    fig_gender.update_layout(margin=dict(l=0, r=0, t=20), height=200,template='plotly_dark')
    fig_income_date.update_layout(margin=dict(l=0, r=0, t=20), height=300,template='plotly_dark')
    fig_product_income.update_layout(margin=dict(l=0, r=0, t=20), height=300,template='plotly_dark')
    
    return fig_city, fig_payment, fig_gender, fig_product_income, fig_income_date




if __name__ == "__main__":
    app.run_server(debug=False)
#app.run_server(debug=False, port=8051)
