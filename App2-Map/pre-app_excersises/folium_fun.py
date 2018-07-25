import folium

markup1 = folium.Marker(location=[49.574, 21.868], popup="The town of Rymanow", icon=folium.Icon(color='blue'))
markup2 = folium.Marker(location=[50.174, 19.868], popup="An unknown place", icon=folium.Icon(color='red'))
fg = folium.FeatureGroup(name="Map of Poland")

my_map = folium.Map(location=[49.574, 21.868], zoom_start=6, min_zoom=5, max_zoom=9, tiles="Mapbox Bright")
my_map.add_child(markup1)
my_map.add_child(markup2)

my_map.add_child(fg)

my_map.save("res/Map1.html")
