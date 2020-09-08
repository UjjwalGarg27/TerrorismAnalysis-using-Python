
# All Libraries Used
import pandas as pd
import webbrowser

import dash
import dash_html_components as html
from dash.dependencies import Input, State, Output 
import dash_core_components as dcc 
import plotly.graph_objects as go  
import plotly.express as px
from dash.exceptions import PreventUpdate


app = dash.Dash()

# CSS Classes
tabs_styles = {
    'height': '100px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '20px'
}


def load_data():
  dataset_name = "H:\PROJECT - Forsk Coding School\Training\global_terror1.csv"

  pd.options.mode.chained_assignment = None
  # Hide warnings, if any
  
  global df
  df = pd.read_csv(dataset_name)
  
  global month_list
  month = {
             "January":1,
             "February": 2,
             "March": 3,
             "April":4,
             "May":5,
             "June":6,
             "July": 7,
             "August":8,
             "September":9,
             "October":10,
             "November":11,
             "December":12
          }
  month_list= [{"label":key, "value":values} for key,values in month.items()]

  global date_list
  date_list = [x for x in range(1, 32)]
  # Other ways to write
  # date_list(range(1,32))
  # date_list = [{"label":x, "value":x} for x in range(1, 32)]


  global region_list
  region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
  # Total 12 Regions

  global country_list
  # Total 205 Countries
  country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()

  global state_list
  # Total 2580 states
  state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()

  global city_list
  # Total 39489 cities
  city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()

  global attack_type_list
  attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]
  
  global year_list
  year_list = sorted ( df['iyear'].unique().tolist()  )

  global year_dict
  year_dict = {str(year): str(year) for year in year_list}
  
  
  global chart_dropdown_values
  chart_dropdown_values = {"Terrorist Organisation":'gname', "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', "Region":'region_txt', "Country Attacked":'country_txt'
                          }
                              
  chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
  
def open_browser():
  webbrowser.open_new('http://127.0.0.1:8050/')


def create_app1_ui():
  # UI of the Webpage
  main_layout = html.Div(id="body", style={'background': 'khaki'}, children= [
  html.H1('Terrorism Analysis with Insights', id='Main_title', style={'background': 'beige', 'textAlign': 'center', 'color': 'blue', 'fontSize': 60}),
  dcc.Tabs(id="Tabs", value="Map", children=[
      dcc.Tab(label="Map Tool" ,id="Map tool",value="Map", style=tab_style, selected_style=tab_selected_style, children=[
          dcc.Tabs(id = "subtabs", value = "WorldMap", children = [
              dcc.Tab(label="World Map Tool", id="World", value="WorldMap", style=tab_style, selected_style=tab_selected_style),
              dcc.Tab(label="India Map Tool", id="India", value="IndiaMap", style=tab_style, selected_style=tab_selected_style)
              ]),
          html.Br(),
          dcc.Dropdown(
              id='month', 
                options=month_list,
                placeholder='SELECT MONTH',
                multi = True,
                style = {'background': 'beige', 'borderColor': 'black', 'borderRadius': '6px', 'color': 'green',
                         'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                  ),
          dcc.Dropdown(
                id='date', 
                placeholder='SELECT DAY',
                multi = True,
                style = {'background': 'beige', 'borderColor': 'black', 'borderRadius': '6px', 'color': 'green',
                         'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                  ),
          dcc.Dropdown(
                id='region-dropdown', 
                options=region_list,
                placeholder='SELECT REGION',
                multi = True,
                style = {'background': 'beige', 'borderColor': 'black', 'borderRadius': '6px', 'color': 'green',
                         'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                  ),
          dcc.Dropdown(
                id='country-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='SELECT COUNTRY',
                multi = True,
                style = {'background': 'beige', 'borderColor': 'black', 'borderRadius': '6px', 'color': 'green',
                         'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                  ),
          dcc.Dropdown(
                id='state-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='SELECT STATE OR PROVINCE',
                multi = True,
                style = {'background': 'beige', 'borderColor': 'black', 'borderRadius': '6px', 'color': 'green',
                         'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                  ),
          dcc.Dropdown(
                id='city-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='SELECT CITY',
                multi = True,
                style = {'background': 'beige', 'borderColor': 'black', 'borderRadius': '6px', 'color': 'green',
                         'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                  ),
          dcc.Dropdown(
                id='attacktype-dropdown', 
                options=attack_type_list,#[{'label': 'All', 'value': 'All'}],
                placeholder='SELECT ATTACK TYPE',
                multi = True,
                style = {'background': 'beige', 'borderColor': 'black', 'borderRadius': '6px', 'color': 'green',
                         'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                  ),

          html.H5('SELECT THE YEAR', id='year_title', style = {'background': 'beige', 'textAlign': 'center', 
                                                               'color': 'grey', 'fontSize': 20}),
          dcc.RangeSlider(
                    id='year-slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),
          html.Br()
    ]),
      dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", style=tab_style, selected_style=tab_selected_style, children=[
          dcc.Tabs(id = "subtabs2", value = "WorldChart",children = [
              dcc.Tab(label="World Chart Tool", id="WorldC", value="WorldChart", style=tab_style, selected_style=tab_selected_style),          
            dcc.Tab(label="India Chart Tool", id="IndiaC", value="IndiaChart", style=tab_style, selected_style=tab_selected_style)]),
            html.Br(),
            dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt",
                         style = {'background': 'beige', 'borderColor': 'black', 'borderRadius': '6px', 'color': 'green', 
                                  'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}), 
            html.Br(),
            html.Hr(),
            dcc.Input(id="search", placeholder="Search Filter", style={'background': 'beige', 'borderColor': 'black', 
                                                                       'borderRadius': '6px', 'color': 'green', 'padding': '11px', 
                                                                       'width': '63%', 'margin-left': '18%', 'textAlign': 'center'}),
            html.Hr(),
            html.Br(),
            dcc.RangeSlider(
                    id='cyear_slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),
                  html.Br()
              ]),
         ]),
  html.Div(id = "graph-object", children ="Graph will be shown here", style={'background': 'beige', 'textAlign': 'center', 
                                                                             'color': 'grey', 'fontSize': 20})
  ])
        
  return main_layout


# All Callback Used
@app.callback(dash.dependencies.Output('graph-object', 'children'),
    [
     dash.dependencies.Input("Tabs", "value"),
    dash.dependencies.Input('month', 'value'),
    dash.dependencies.Input('date', 'value'),
    dash.dependencies.Input('region-dropdown', 'value'),
    dash.dependencies.Input('country-dropdown', 'value'),
    dash.dependencies.Input('state-dropdown', 'value'),
    dash.dependencies.Input('city-dropdown', 'value'),
    dash.dependencies.Input('attacktype-dropdown', 'value'),
    dash.dependencies.Input('year-slider', 'value'), 
    dash.dependencies.Input('cyear_slider', 'value'), 
    
    dash.dependencies.Input("Chart_Dropdown", "value"),
    dash.dependencies.Input("search", "value"),
    dash.dependencies.Input("subtabs2", "value")
    ]
    )

def update_app2_ui(Tabs, month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,
                   chart_year_selector, chart_dp_value, search,subtabs2):
    fig = None
     
    if Tabs == "Map":
        
        year_range = range(year_value[0], year_value[1]+1)
        new_df = df[df["iyear"].isin(year_range)]
        
        
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[new_df["imonth"].isin(month_value)
                                & (new_df["iday"].isin(date_value))]
        
        
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None :
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))&
                        (new_df["city"].isin(city_value))]
                        
        if attack_value == [] or attack_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)] 
        
        
               
        mapFigure = go.Figure()
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(new_df,
          lat="latitude", 
          lon="longitude",
          color="attacktype1_txt",
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1
          )
        mapFigure.update_layout(mapbox_style="open-street-map",
          autosize=True,
          margin=dict(l=0, r=0, t=25, b=20),
          )
          
        fig = mapFigure

    elif Tabs=="Chart":
        fig = None
        
        
        year_range_c = range(chart_year_selector[0], chart_year_selector[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])
            
            chart_df.loc[0] = [0, 0,"No data"]
        chartFigure = px.area(chart_df, x="iyear", y ="count", color = chart_dp_value)
        fig = chartFigure
    return dcc.Graph(figure = fig)



@app.callback(
  Output("date", "options"),
  [Input("month", "value")])

def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option

@app.callback([Output("region-dropdown", "value"),
               Output("region-dropdown", "disabled"),
               Output("country-dropdown", "value"),
               Output("country-dropdown", "disabled")],
              [Input("subtabs", "value")])

def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c

@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')])

def set_country_options(region_value):
    option = []
    # Country Dropdown Data
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])

def set_state_options(country_value):
  # State Dropdown Data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]

@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])

def set_city_options(state_value):
  # City Dropdown Data
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]


def main():
  load_data()
  
  open_browser()
  
  global app
  app.layout = create_app1_ui()
  app.title = "Terrorism Analysis with Insights"
  
  app.run_server()
  # It will run for infinite time so, don't write any statement after this

  print("This would be executed only after the script is closed")
  df = None
  app = None

# Do not write anything here

if __name__ == '__main__':
    main()

