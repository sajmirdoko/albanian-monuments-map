import pandas as pd #data frame operations
import numpy as np #arrays and math functions
from scipy.stats import uniform #for training and test splits
import statsmodels.api as smf #R-like model specification
import matplotlib.pyplot as plt #2D plotting
import requests
import folium
import sys
import math
from folium.plugins import FeatureGroupSubGroup
from folium.plugins import MarkerCluster
import geopandas as gpd
from shapely.geometry import Point
from folium.plugins import MeasureControl
from datetime import datetime
from folium.plugins import TimestampedGeoJson
import json

albania = pd.read_csv("monuments-in-albania.csv")
# albania.rename(columns = albania.iloc[0]).drop(albania.index[0])

# albania.columns = ['event_date', 'event_year', 'event_type', 'subevent_type', 'actor1', 'admin1', 'location', 'latitude', 'longitude', 'notes']

# albania = albania.drop(albania.index[[0]])

# albania = albania[['event_date', 'event_year', 'event_type', 'subevent_type', 'actor1', 'admin1', 'location', 'latitude', 'longitude', 'notes']]

albania['longitude'] = albania['longitude'].astype(float)
albania['latitude'] = albania['latitude'].astype(float)

# x = np.unique(albania.event_type)
#albania.info()
#albania.head()
# viol = albania[~albania["event_type"].isin(["Strategic developments", "Protests"])]
# peace = albania[albania["event_type"].isin(["Strategic developments", "Protests"])]

# albania["event_date"]  =  pd.to_datetime(albania["event_date"])

# churches  =  albania[albania["monument_type"] == "church"]

# albania.info()
albania.head()
# albania.to_csv(r'albania.csv', index  =  False)

def color(monument_type):
  if monument_type  ==  "castle":
    col = 'blue'
  elif monument_type == "church":
    col = 'orange'
  else:
    col = 'red'
  return col

def icon(monument_type):
  if monument_type  ==  "castle":
    icon = 'fa-bank'
  elif monument_type == "church":
    icon = 'fa-plus-square'
  else:
    icon = 'fa-question-circle'
  return icon

def style_function(feature):
  return {"fillColor": "#0084ff", "color": "red", "weight": 1.5, "dashArray": "5, 5"}

def highlight_function(feature):
  return {"fillColor": "#0084ff", "color": "blue", "weight": 1.5, "dashArray": "5, 5"}


with open('world-countries.json') as handle:
  country_geo = json.loads(handle.read())

for i in country_geo['features']:
  if i['properties']['name'] == 'Albania':
    country = i
    break

eventmap2  =  folium.Map(
    location = [41.00, 20.00],
    zoom_start = 8,
    tiles = 'Stamen Water Color',
    prefer_canvas=True
)
folium.GeoJson(
    country,
    name='albania',
    overlay=True,
    style_function=style_function,
    highlight_function=highlight_function,
  ).add_to(eventmap2)

mcg = folium.plugins.MarkerCluster(name = "monument_name", control = False)
eventmap2.add_child(mcg)

marker_cluster2 = folium.plugins.FeatureGroupSubGroup(mcg, 'church')
eventmap2.add_child(marker_cluster2)

folium.map.CustomPane("labels").add_to(eventmap2)
folium.TileLayer("CartoDBPositronOnlyLabels", pane="labels").add_to(eventmap2)

# '''for _, row in viol.iterrows():
#   html = """<i>Location: </i> <br> <b>{}</b> <br>
#                   <i>Date: </i><b><br>{}</b><br>
#                   <i>Description: </i><b><br>{}</b><br>""".format( row['location'], row['event_date'], row['notes'])
#   iframe = folium.IFrame(html, width = 200, height = 300)
#   popup  =  folium.Popup(iframe, max_width = 500)
#   marker = folium.Marker(
#         location = [row['latitude'], row['longitude']],
#         popup = popup,
#         icon = folium.Icon(color = color(row['event_type']), icon = icon(row['event_type']), prefix = 'fa', icon_color = 'black')).add_to(marker_cluster)'''


# '''for _, row in peace.iterrows():
#   html = """<i>Location: </i> <br> <b>{}</b> <br>
#                   <i>Date: </i><b><br>{}</b><br>
#                   <i>Description: </i><b><br>{}</b><br>""".format( row['location'], row['event_date'], row['notes'])
#   iframe = folium.IFrame(html, width = 200, height = 300)
#   popup  =  folium.Popup(iframe, max_width = 500)
#   marker = folium.Marker(
#         location = [row['latitude'], row['longitude']],
#         popup = popup,
#         icon = folium.Icon(color = color(row['event_type']), icon = icon(row['event_type']), prefix = 'fa', icon_color = 'black')).add_to(marker_cluster1)'''

for _, row in albania.iterrows():
  html = """Location: {}<br> Description: {}""".format( row['city'], row['notes'])

  iframe = folium.IFrame(html, width = 300, height = 200)
  popup  =  folium.Popup(iframe, max_width = 500)
  marker = folium.Marker(
        location = [row['latitude'], row['longitude']],
        popup = popup,
        # tooltip='Click for details!',
        icon = folium.Icon(
          color = color(row['monument_type']),
          icon = icon(row['monument_type']),
          prefix = 'fa',
          icon_color = 'black'
        )
      ).add_to(marker_cluster2)


# folium.TileLayer("OpenStreetMap").add_to(eventmap2)
# folium.TileLayer("cartodbdark_matter").add_to(eventmap2)
# folium.TileLayer("cartodbpositron").add_to(eventmap2)
# folium.TileLayer('Stamen Terrain').add_to(eventmap2)
# folium.TileLayer('Stamen Toner').add_to(eventmap2)
# folium.TileLayer('Stamen Water Color').add_to(eventmap2)
# folium.TileLayer('cartodbpositron').add_to(eventmap2)
# folium.LayerControl().add_to(eventmap2)

# eventmap2
eventmap2.save('index.html')