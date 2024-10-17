import pandas as pd 
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
df = pd.read_csv(URL)

app = Dash()

app.layout = [
    html.Div([
        html.H1('Automobile Sales Statistics Dashboard', style= {'textAlign':'center', 'color':'#503D36', 'font-size':24}),
        dcc.Dropdown(options= [{'label':'Yearly Statistics','value':0},
                               {'label':'Recession Period Statistics', 'value':1}],
                               placeholder= 'Select a report type',
                               value= 'Select Statistic',
                               id= 'dropdown-statistic'),
        dcc.Dropdown(options= [{'label': i, 'value':i} for i in df['Year'].unique()],
                     placeholder='Select-Year',
                     value='Select-Year',
                     id='select-year'),
        html.Div([
            html.Div(
                 className='chart-grid',
                 style={'display':'grid', 'grid-template-columns': '1fr 1fr'},
                 id='output-container'),
                 ])
    ])
]

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistic',component_property='value')
)

def update_input_container(value):
    if value == 0:
        return False
    else:
        return True
    
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistic', component_property= 'value'), Input(component_id='select-year', component_property='value')]
)

def update_output_container(stat, year):
    if stat == 1:
        recession = df[df['Recession']==1]

        # Line chart
        group = recession.groupby(by=['Year'],as_index=False).agg({'Automobile_Sales':'mean'})
        plot1 = dcc.Graph(figure=px.line(group, x='Year', y='Automobile_Sales', title= 'Sales fluctuation during recession period'))

        # Bar chart
        group2 = recession.groupby(by=['Vehicle_Type'], as_index=False).agg({'Automobile_Sales':'sum'})
        plot2 = dcc.Graph(figure=px.bar(group2, x='Vehicle_Type', y='Automobile_Sales', title='Sales of  Vehicle type during recession period'))

        # Pie chart
        group3 = recession.groupby(by=['Vehicle_Type'], as_index=False).agg({'Advertising_Expenditure':'sum'})
        plot3 = dcc.Graph(figure=px.pie(group3, names='Vehicle_Type',values='Advertising_Expenditure', title='Total Expenditure share by vehicle type during recession period' ))

        # Bar chart
        group4 = recession.groupby(by=['unemployment_rate','Vehicle_Type'], as_index=False).agg({'Automobile_Sales':'mean'})
        plot4 = dcc.Graph(figure=px.bar(group4, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                                        labels={'unemployment_rate':'Unemployment Rate', 
                                                'Automobile_Sales':'Average Automobile Sales'},
                                        title= 'Average Automobile Sales by Unemployment Rate and Vehicle Type'))
        
        return [
            # html.Div(className='chart-item', children=[html.Div(children=plot1),html.Div(children=plot2)], style={'display':'flex'}),
            # html.Div(className='chart-item', children=[html.Div(children=plot3),html.Div(children=plot4)], style={'display':'flex'})
                html.Div(className='chart-item', children=plot1),
                html.Div(className='chart-item', children=plot2),

                # Segunda fila con dos gráficos
                html.Div(className='chart-item', children=plot3),
                html.Div(className='chart-item', children=plot4)
        ]
    elif (year and stat == 0):
        yearly_data = df[df['Year']== year]

        # Line chart
        group5 = df.groupby(by=['Year'], as_index=False).agg({'Automobile_Sales':'sum'})
        plot5 = dcc.Graph(figure=px.line(group5,x='Year',y='Automobile_Sales', title='Yearly Automobile Sales'))

        # Line chart
        group6 = df.groupby(by=['Month'], as_index=False).agg({'Automobile_Sales':'sum'})
        plot6 = dcc.Graph(figure=px.line(group6, x='Month', y='Automobile_Sales', title= 'Total Sales by Month'))

        # Bar chart
        group7 = yearly_data.groupby(by=['Vehicle_Type'],as_index=False).agg({'Automobile_Sales':'mean'})
        plot7 = dcc.Graph(figure=px.bar(group7, x='Vehicle_Type',y='Automobile_Sales', title=f'Average Vehicles sold by Vehicle Type in the year {year}'))

        # Pie chart
        group8 = yearly_data.groupby(by=['Vehicle_Type'], as_index = False).agg({'Advertising_Expenditure': 'sum'})
        plot8 = dcc.Graph(figure= px.pie(group8, names='Vehicle_Type', values='Advertising_Expenditure', title=f'Total Advertising Expenditure for each Vehicle in year {year}'))

        return [
                html.Div(className='chart-item', children=plot5),
                html.Div(className='chart-item', children=plot6),

                # Segunda fila con dos gráficos
                html.Div(className='chart-item', children=plot7),
                html.Div(className='chart-item', children=plot8)
        ]
    
if __name__ == '__main__':
    app.run_server()
