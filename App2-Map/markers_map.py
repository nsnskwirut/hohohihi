import json

import folium
import pandas

volcano_data = pandas.read_csv("res/Volcanoes_USA.csv")
lon_from_csv = list(volcano_data["LON"])
lat_from_csv = list(volcano_data["LAT"])
name_from_csv = list(volcano_data["NAME"])
elev_from_csv = list(volcano_data["ELEV"])


def open_json(path, mode='r'):
    with open(path, mode) as f:
        content = json.load(f, encoding='utf-8-sig')
    return content


def determine_color(height):
    if height < 1000:
        return 'lightgreen'
    elif height < 2000:
        return 'green'
    elif height < 3000:
        return 'orange'
    elif height < 4000:
        return 'red'
    else:
        return 'darkred'


mymap = folium.Map(location=[38.58, -99.09], zoom_start=6, max_zoom=9, min_zoom=0)

mymap_fg_pop = folium.FeatureGroup(name="USA state population")
mymap_fg_pop.add_child(folium.GeoJson(open_json('res/usa_states.json'),
                                      style_function=lambda x:
                                      {'fillColor': 'lightgreen' if x['properties']['POP'] in range(0, 5*10**5)
                                      else 'green'    if x['properties']['POP'] in range(5*10**5+1, 1*10**6)
                                      else 'blue'     if x['properties']['POP'] in range(1*10**6+1, 3*10**6)
                                      else 'purple'   if x['properties']['POP'] in range(3*10**6+1, 5*10**6)
                                      else 'yellow'   if x['properties']['POP'] in range(5*10**6+1, 10*10**6)
                                      else 'pink'     if x['properties']['POP'] in range(10*10**6+1, 15*10**6)
                                      else 'red'      if x['properties']['POP'] in range(15*10**6+1, 20*10**6)
                                      else 'darkred'  if x['properties']['POP'] > 30*10**6+1
                                      else 'brown',
                                      'color': 'grey',
                                      'weigth': 0.5,
                                      'dashArray': '5, 10'
                                      },
                                      highlight_function=lambda x:{'fillColor': 'grey', 'color': 'white'},
                                      ))
mymap.add_child(mymap_fg_pop)


mymap_fg_vol = folium.FeatureGroup(name="Volcanoes in the USA")
for lt, ln, nm, elev in zip(lat_from_csv, lon_from_csv, name_from_csv, elev_from_csv):
    vol_markup = folium.CircleMarker(location=[lt, ln],
                                 popup="{}, {}m high".format(nm, int(elev)),  # popup=folium.Popup(nm, parse_html=True)
                                 fill_color=determine_color(elev),
                                 color=None,
                                 radius=8,
                                 fill_opacity=0.7,
                                 fill=True
                                 )
    mymap_fg_vol.add_child(vol_markup)
mymap.add_child(mymap_fg_vol)


mymap.add_child(folium.LayerControl())
mymap.save('res/volcanoes_map.html')

