import sqlite3
from sqlite3 import Error
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import folium


conn = sqlite3.connect('../data/rodents_data.db')
sql_statement = """SELECT latitude,longitude,count(inspection_date) as recurrence_index FROM 'rodent_incidents' where inspection_date > '2008-12-31' GROUP BY latitude,longitude order by inspection_date"""
overall_location_based_data = pd.read_sql_query(sql_statement, conn)

sql_statement = """SELECT * from (SELECT strftime("%Y/%m", inspection_date) as 'year_month',count(inspection_date) as incidents  FROM (SELECT inspection_date FROM 'rodent_incidents' where inspection_date > '2008-12-31' order by inspection_date) GROUP BY strftime("%Y/%m", inspection_date)) where incidents > 500"""
monthly_rodent_incidents = pd.read_sql_query(sql_statement, conn)

sql_statement = """SELECT latitude,longitude,strftime("%Y", inspection_date) as 'year',count(inspection_date) as recurrence_index  FROM (SELECT latitude,longitude,inspection_date FROM 'rodent_incidents' where inspection_date > '2008-12-31' order by inspection_date) GROUP BY strftime("%Y", inspection_date),latitude,longitude"""
yearly_location_based_data = pd.read_sql_query(sql_statement, conn)

sql_statement = """SELECT latitude,longitude,strftime("%Y/%m", inspection_date) as 'year_month',count(inspection_date) as recurrence_index  FROM (SELECT latitude,longitude,inspection_date FROM 'rodent_incidents' where inspection_date > '2008-12-31' order by inspection_date) GROUP BY strftime("%Y/%m", inspection_date),latitude,longitude"""
monthly_location_based_data = pd.read_sql_query(sql_statement, conn)
conn.commit()
conn.close()

overall_geospatial_map = folium.Map(location=[40.698027, -73.932098],tiles="CartoDB positron ",zoom_control  = False,min_zoom=10,max_zoom=13, height=500,width=500)
for index,record in overall_location_based_data.iterrows():
    geo_location = [record['latitude'],record['longitude']]
    magnitude = record['recurrence_index']
    if(magnitude < 52):
        circle_color = '#22c92b'
        circle_radius = 2
        circle_text = 2
    elif(magnitude < 186):
        circle_color = '#94c922'
        circle_radius = 2
        circle_text = 2
    elif(magnitude < 764):
        circle_color = '#fcbe03'
        circle_radius = 2.5
        circle_text = 2
    elif(magnitude <= 10000):
        circle_color = '#fc5603'
        circle_radius = 3
        circle_text = 2
    elif(magnitude > 10000):
        circle_color = '#d40000'
        circle_radius = 4
        circle_text = 2
    folium.CircleMarker(location=geo_location,
                   radius= circle_radius,
                   color=circle_color).add_to(overall_geospatial_map)
overall_geospatial_map



yearly_geospatial_map = folium.Map(location=[40.698027, -73.932098],tiles="CartoDB positron",zoom_control  = False)

time_data_points = []

for index,record in yearly_location_based_data.iterrows():
    obj = {
        'time':'',
        'coordinates':[],
        'value':0
        }
    obj['time'] = str(int(record['year']))
    obj['coordinates'] = [record['longitude'],record['latitude']]
    obj['value'] = int(record['recurrence_index'])
    time_data_points.append(obj)
features = [
    {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': point['coordinates'],
        },
        'properties': {
            'time': point['time'],
            'icon': 'circle',
            'iconstyle': {
                'color':'#22c92b' if point['value']<=6 else'#94c922'if point['value'] <=18 else '#fcbe03' if point['value'] <=59 else '#fc5603' if point['value']<= 1200 else '#d40000',
                'fillColor': '#22c92b' if point['value']<=6 else'#94c922'if point['value'] <=18 else '#fcbe03' if point['value'] <=59 else '#fc5603' if point['value']<= 1200 else '#d40000',
                'fillOpacity': 0.6,
                'stroke': 'false',
                'radius': 2 if point['value']<=6 else 2 if point['value'] <=18 else 2.5 if point['value'] <=59 else 3 if point['value']<= 1200 else 4
            },
            'style': {'weight': 1}
        }
    } for point in time_data_points
]

from folium import plugins
plugins.TimestampedGeoJson(
    {
        'type': 'FeatureCollection',
        'features': features
    },
    period='P1Y',
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options='YYYY',
    time_slider_drag_update=True,
    duration='P1Y'
).add_to(yearly_geospatial_map)

yearly_geospatial_map


monthly_geospatial_map = folium.Map(location=[40.698027, -73.932098],tiles="CartoDB positron",zoom_control  = False)

time_data_points = []


for index,record in monthly_location_based_data.iterrows():
    obj = {
        'time':'',
        'coordinates':[],
        'value':0
        }
    obj['time'] = str(record['year_month'])
    obj['coordinates'] = [record['longitude'],record['latitude']]
    obj['value'] = int(record['recurrence_index'])
    time_data_points.append(obj)
features = [
    {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': point['coordinates'],
        },
        'properties': {
            'time': point['time'],
            'icon': 'circle',
            'iconstyle': {
                'color':'#22c92b' if point['value']<=1 else'#94c922'if point['value'] <=3 else '#fcbe03' if point['value'] <=9 else '#fc5603' if point['value']<= 200 else '#d40000',
                'fillColor': '#22c92b' if point['value']<=1 else'#94c922'if point['value'] <=3 else '#fcbe03' if point['value'] <=9 else '#fc5603' if point['value']<= 200 else '#d40000',
                'fillOpacity': 0.6,
                'stroke': 'false',
                'radius': 2 if point['value']<=1 else 2 if point['value'] <=3 else 2.5 if point['value'] <=9 else 3 if point['value']<= 200 else 4
            },
            'style': {'weight': 1}
        }
    } for point in time_data_points
]

from folium import plugins
plugins.TimestampedGeoJson(
    {
        'type': 'FeatureCollection',
        'features': features
    },
    period='P1M',
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options='YYYY/MM',
    time_slider_drag_update=True,
    duration='P1M'
).add_to(monthly_geospatial_map)

monthly_geospatial_map


monthly_rodent_incidents.index = pd.to_datetime(monthly_rodent_incidents['year_month'], format='%Y/%m')
monthly_rodent_incidents.drop(['year_month'], axis=1,inplace = True)
plt.plot(monthly_rodent_incidents.incidents, label='Occurrences',linewidth=1.5)
plt.title('Rodent Incidents from 2009-2019')
plt.xlabel('Years')
plt.legend()
fig= plt.figure(figsize=(20,10))
plt.show()

monthly_rodent_incidents.incidents.rolling(12).mean().plot(figsize=(20,10), linewidth=5, fontsize=20)
plt.show()

from pylab import rcParams
rcParams['figure.figsize'] = 11, 9
result = sm.tsa.seasonal_decompose(monthly_rodent_incidents.incidents, model='additive', period=12)
result.plot()
plt.show()


pd.plotting.autocorrelation_plot(monthly_rodent_incidents.incidents)
plt.show()

pd.plotting.lag_plot(monthly_rodent_incidents.incidents)
plt.show()

def adfuller_test(series, title=''):
    dfout={}
    dftest=sm.tsa.adfuller(series.dropna(), autolag='AIC', regression='ct')
    for key,val in dftest[4].items():
        dfout[f'critical value ({key})']=val
    # print(dftest)
    if dftest[1]<=0.06:
        print("Data is Stationary for", title)
    else:
        print("Data is NOT Stationary for", title)
adfuller_test(monthly_rodent_incidents.incidents, "Rodent Incidents")

mod = sm.tsa.SARIMAX(monthly_rodent_incidents.incidents, trend='n',freq='MS', order=(3,1,3), seasonal_order=(1,1,1,12))
results = mod.fit()

monthly_rodent_incidents['forecast'] = results.predict(start = 100, end= 120, dynamic= True)  
monthly_rodent_incidents[['incidents', 'forecast']].plot(figsize=(12, 8))
plt.show()


def predict_rodent_incidents(df, months_to_predict):
    df_perdict = df.reset_index()
    months = df_perdict['year_month']
    months = months + pd.DateOffset(months = months_to_predict)
    to_be_predicted_dates = months[-months_to_predict -1:]
    df_perdict = df_perdict.set_index('year_month')
    future = pd.DataFrame(index=to_be_predicted_dates, columns= df_perdict.columns)
    df_perdict = pd.concat([df_perdict, future])
    df_perdict['forecast'] = results.predict(start = 123, end = 160, dynamic= True)  
    df_perdict[['incidents', 'forecast']].iloc[-months_to_predict - 125:].plot(figsize=(16, 12))
    plt.show()
    return df_perdict[-months_to_predict:]

predicted = predict_rodent_incidents(monthly_rodent_incidents.incidents,24)