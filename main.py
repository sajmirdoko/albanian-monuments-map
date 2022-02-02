import pandas as pd  # data frame operations
import numpy as np  # arrays and math functions
from scipy.stats import uniform  # for training and test splits
import statsmodels.api as smf  # R-like model specification
import matplotlib.pyplot as plt  # 2D plotting
import folium
from folium.plugins import FeatureGroupSubGroup
from folium.plugins import MarkerCluster
import geopandas as gpd
from shapely.geometry import Point
from folium.plugins import MeasureControl
from datetime import datetime
from folium.plugins import TimestampedGeoJson
import json

albania = pd.read_csv("monuments-in-albania.csv")

albania['longitude'] = albania['longitude'].astype(float)
albania['latitude'] = albania['latitude'].astype(float)

# albania.info()
albania.head()


def color(monument_type):
    if monument_type == "castle":
        col = 'blue'
    elif monument_type == "church":
        col = 'orange'
    else:
        col = 'red'
    return col


def icon(monument_type):
    if monument_type == "castle":
        icon = 'fa-bank'
    elif monument_type == "church":
        icon = 'fa-plus-square'
    else:
        icon = 'fa-question-circle'
    return icon


colors = {"Berat": "#DFFF00", "Dibër": "#CACFD2", "Durrës": "#FFBF00", "Elbasan": "#DE3163", "Fier": "#40E0D0", "Gjirokastër": "#9FE2BF",
          "Korçë": "#6495ED", "Kukës": "#2C3E50", "Lezhë": "#FA8072", "Shkodër": "#138D75", "Tiranë": "#5499C7", "Vlorë": "#FF7F50"}


def style_function(feature):
    city = feature['properties']['name_1']
    ret = {}
    ret["Fillcolor"] = "black"
    ret["weight"] = 1.5
    ret["dashArray"] = "5, 5"
    ret["color"] = colors[city]
    return ret


def highlight_function(feature):
    return {"fillColor": "blue"}


with open('world-countries.json') as handle:
    country_geo = json.loads(handle.read())

# for i in country_geo['features']:
#   if i['properties']['name'] == 'Albania':
#     country = i
#     break

eventmap2 = folium.Map(
    location=[41.00, 20.00],
    zoom_start=8,
    tiles='Stamen Water Color',
    prefer_canvas=True
)
folium.GeoJson(
    country_geo,
    name='albania',
    overlay=True,
    style_function=style_function,
    highlight_function=highlight_function,
).add_to(eventmap2)

mcg = folium.plugins.MarkerCluster(name="monument_name", control=False)
eventmap2.add_child(mcg)

marker_cluster2 = folium.plugins.FeatureGroupSubGroup(mcg, 'church')
eventmap2.add_child(marker_cluster2)

folium.map.CustomPane("labels").add_to(eventmap2)
folium.TileLayer("CartoDBPositronOnlyLabels", pane="labels").add_to(eventmap2)

for _, row in albania.iterrows():
    html = """Location: {}<br> Description: {}""".format(
        row['city'], row['notes'])

    iframe = folium.IFrame(html, width=300, height=200)
    popup = folium.Popup(iframe, max_width=500)
    marker = folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup,
        # tooltip='Click for details!',
        icon=folium.Icon(
            color=color(row['monument_type']),
            icon=icon(row['monument_type']),
            prefix='fa',
            icon_color='black'
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
