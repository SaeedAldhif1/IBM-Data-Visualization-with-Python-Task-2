#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Load the data using pandas
data = pd.read_csv(r"C:\Users\saeed\Downloads\historical_automobile_sales(1).csv")

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={"textAlign": "left", "color": "#000000", "font-size": 0}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type',
            style={"textAlign": "center", "padding": "3px", "font-size": "20px"}
        ),
    ]),
    html.Div(
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            multi=True,
            value=[i for i in range(1980, 2024, 1)]
        )),
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ])
])

# Callback to update the "select-year" dropdown based on selected statistics
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    return not selected_statistics == 'Recession Period Statistics'

# Callback for plotting graphs
@app.callback(
    Output('output-container', 'children'),
    Input('select-year', 'value'),
    Input('dropdown-statistics', 'value')
)
def update_output_container(year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over Recession Period (year-wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Automobile Sales Fluctuation Over Recession Period"
            )
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type
        average_sales = data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title='Average Vehicles Sold by Type'))

        # Plot 3: Pie chart for total advertising expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Advertising Expenditure Share by Vehicle Type During Recessions"
            )
        )

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        vehicle_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()
        unemployment_rate = recession_data.groupby('Vehicle_Type')['unemployment_rate'].mean().reset_index()

        # Create a Figure object for vehicle sales
        sales_figure = go.Figure(data=[go.Bar(x=vehicle_sales['Vehicle_Type'], y=vehicle_sales['Automobile_Sales'])])
        sales_figure.update_layout(title='Vehicle Sales by Type', xaxis_title='Vehicle Type', yaxis_title='Sales')

        # Create a Figure object for unemployment rate
        unemployment_figure = go.Figure(data=[go.Bar(x=unemployment_rate['Vehicle_Type'], y=unemployment_rate['unemployment_rate'])])
        unemployment_figure.update_layout(title='Unemployment Rate by Vehicle Type', xaxis_title='Vehicle Type', yaxis_title='Unemployment Rate')

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children='Description for Sales Chart')],
                     style={'width': '50%', 'display': 'inline-block'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart2), html.Div(children='Description for Unemployment Chart')],
                     style={'width': '50%', 'display': 'inline-block'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children='Description for Expenditure Chart')],
                     style={'width': '50%', 'display': 'inline-block'}),
            html.Div(className='chart-item', children=[dcc.Graph(figure=sales_figure), html.Div(children='Description for Vehicle Sales Chart')],
                     style={'width': '50%', 'display': 'inline-block'}),
            html.Div(className='chart-item', children=[dcc.Graph(figure=unemployment_figure), html.Div(children='Description for Unemployment Rate Chart')],
                     style={'width': '50%', 'display': 'inline-block'}),
        ]

    elif year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'].isin(year)]

        # Plot 1: Yearly Automobile sales using line chart for the whole period.
        yearly_sales_data = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yearly_sales_data, x='Year', y='Automobile_Sales', title="Yearly Automobile Sales"))

        # Plot 2: Total Monthly Automobile sales using line chart.
        monthly_sales_data = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(monthly_sales_data, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales'))

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        average_vehicle_data = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(average_vehicle_data, x='Vehicle_Type', y='Automobile_Sales', title='Average Vehicles Sold by Vehicle Type'))

        # Plot 4: Pie chart for total advertising expenditure by vehicle type
        expenditure_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(expenditure_data, values='Advertising_Expenditure', names='Vehicle_Type', title='Total Advertising Expenditure by Vehicle Type'))

        return [
            html.Div(className='chart-item', children=[dcc.Graph(figure=Y_chart1), html.Div(children='Description for Sales Chart')],
                     style={'width': '50%', 'display': 'inline-block'}),
            html.Div(className='chart-item', children=[dcc.Graph(figure=Y_chart2), html.Div(children='Description for Monthly Sales Chart')],
                     style={'width': '50%', 'display': 'inline-block'}),
            html.Div(className='chart-item', children=[dcc.Graph(figure=Y_chart3), html.Div(children='Description for Average Vehicle Sales Chart')],
                     style={'width': '50%', 'display': 'inline-block'}),
            html.Div(className='chart-item', children=[dcc.Graph(figure=Y_chart4), html.Div(children='Description for Advertisement Expenditure Chart')],
                     style={'width': '50%', 'display': 'inline-block'}),
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)