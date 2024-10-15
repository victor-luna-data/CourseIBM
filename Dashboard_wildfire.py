import pandas as pd 
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import datetime as dt

app = dash.Dash(__name__)

df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year 

region_options = [{'label':region, 'value':region} for region in df['Region'].unique()]
year_options = df['Year'].unique()

app.layout = html.Div(
    children=[
        html.H1('Dashborad: Wildfire'),
              
              html.Div([
                  html.H2('Region'),  # Header from slicer RadioItems
                  dcc.RadioItems(id='radio-items',
                                 options= region_options,
                                 value= df['Region'].unique()[0],
                                 inline= True)
              ], style={'display': 'flex', 'align-items': 'center'}),

              html.Div([ # Slicer Year
                  html.H2('Year'),
                  dcc.Dropdown(id='Year-dropdown',
                               options= year_options,
                               value=df['Year'].unique()[0])
              ]),

              html.Div([ # Plots
                html.Div([], id='pie-plot'),
                html.Div([], id='bar-plot')],
                style= {'display': 'flex'})

              ]
)

@app.callback([Output(component_id='pie-plot', component_property='children'),
               Output(component_id='bar-plot', component_property='children')],
               [Input(component_id= 'radio-items', component_property='value'),
                Input(component_id= 'Year-dropdown', component_property= 'value')])

def region_year_plot(input1, input2):
    data = df[(df['Region']==input1) & (df['Year']==input2)]

    group = data.groupby(by=['Month']).agg({'Estimated_fire_area':'mean'}).reset_index()
    fig1 = px.pie(group, values='Estimated_fire_area', names='Month', title=f'{input1}: Monthly Average Estimated Fire Area in year {input2}')
    
    group2 = data.groupby(by=['Month']).agg({'Year':'count'}).rename({'Year':'Count'}, axis = 1).reset_index()
    fig2 = px.bar(group2,x='Month', y='Count', title= f'{input1}: Average Count of Pixels for Presumed Vegetation Fires in year {input2}')

    return [dcc.Graph(figure=fig1), dcc.Graph(figure= fig2)]

if __name__ == '__main__':
    app.run_server()