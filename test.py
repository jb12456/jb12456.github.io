import folium

# Grundkarte erstellen (Zentrum Europa, Zoomstufe 4)
m = folium.Map(location=[50, 10], zoom_start=4, tiles="OpenStreetMap")

# Optional: weitere Basiskarten hinzufügen
folium.TileLayer("CartoDB positron", name="Carto Light").add_to(m)

# Karte speichern
m.save("map_1_basiskarte.html")
print("Gespeichert: map_1_basiskarte.html")

import folium
from folium import Popup, Icon

# Grundkarte
m = folium.Map(location=[50, 8], zoom_start=7, tiles="OpenStreetMap")
folium.TileLayer("CartoDB positron", name="Carto Light").add_to(m)

# Marker: Titel, (lat, lon), Farbe, Icon, Popup-HTML
punkte = [
    ("Mainz", (49.9929, 8.2473), "red", "info-sign", "<strong>Mainz</strong><br>Studium/Ort"),
    ("Frankfurt", (50.1109, 8.6821), "blue", "cloud", "<strong>Frankfurt</strong><br>Große Stadt"),
    ("Koblenz", (50.3569, 7.5886), "green", "ok", "<strong>Koblenz</strong><br>Rhein & Mosel")
]

bounds = []
for titel, (lat, lon), farbe, icon_name, html in punkte:
    popup = Popup(html, max_width=250)
    icon = Icon(color=farbe, icon=icon_name)
    folium.Marker(location=[lat, lon], popup=popup, tooltip=titel, icon=icon).add_to(m)
    bounds.append([lat, lon])

if bounds:
    m.fit_bounds(bounds, padding=(20, 20))

folium.LayerControl(collapsed=False).add_to(m)

# Karte speichern
m.save("map_2_punkte.html")
print("Gespeichert: map_punkte.html")


import folium
from folium.features import DivIcon

# Grundkarte über Rheinland
m = folium.Map(location=[50, 8], zoom_start=8, tiles="OpenStreetMap")
folium.TileLayer("CartoDB positron", name="Carto Light").add_to(m)

# Reiseroute (in Reihenfolge)
route = [
    ("Mainz", (49.9929, 8.2473)),
    ("Koblenz", (50.3569, 7.5886)),
    ("Frankfurt", (50.1109, 8.6821)),
]

# Polyline einzeichnen
coords = [coord for name, coord in route]
folium.PolyLine(locations=coords, color="#0ea5e9", weight=4, opacity=0.8).add_to(m)

# Stationen nummerieren + Marker mit Tooltip/Popup
for i, (name, (lat, lon)) in enumerate(route, start=1):
    folium.map.Marker(
        [lat, lon],
        icon=DivIcon(icon_size=(30,30), icon_anchor=(15,15), html=f"<div style='font-size:12px; font-weight:700; color:#fff; background:#0ea5e9; width:26px; height:26px; line-height:26px; text-align:center; border-radius:50%;'>{i}</div>"
    )).add_to(m)

    # zusätzlicher Marker mit Tooltip/Popup
    folium.Marker([lat, lon], popup=f"<strong>{name}</strong>", tooltip=name).add_to(m)

# Karte speichern
m.save("map_3_reiseroute.html")
print("Gespeichert: map_3_reiseroute.html")

import folium
import requests
from folium import GeoJson

# 1) Welt-GeoJSON ONLINE laden (kein lokaler Download nötig)
url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
resp = requests.get(url)
resp.raise_for_status()
geojson_data = resp.json()

# 2) Menge der besuchten Länder – Namen müssen zum GeoJSON passen
#    In dieser Datei heißt das Namensfeld i. d. R. 'ADMIN' oder 'ADMIN0' ist nicht present; this file uses 'ADMIN' not present, use 'ADMIN' fallback to 'name' -> check properties
visited = {"Germany", "Austria", "Switzerland"}

# 3) Karte anlegen
m = folium.Map(location=[20, 0], zoom_start=2, tiles="OpenStreetMap")
folium.TileLayer("CartoDB positron", name="Carto Light").add_to(m)

# 4) Styling-Funktionen
def style_fn(feature):
    props = feature.get("properties", {})
    country = props.get("ADMIN") or props.get("name") or props.get("NAME") or ""
    if country in visited:
        return {"fillColor": "#22c55e", "color": "#065f46", "weight": 1, "fillOpacity": 0.6}
    return {"fillColor": "#94a3b8", "color": "#334155", "weight": 0.5, "fillOpacity": 0.15}

def highlight_fn(_):
    return {"fillOpacity": 0.8, "weight": 2, "color": "#0ea5e9"}

# 5) GeoJSON zur Karte hinzufügen
GeoJson(
    data=geojson_data,
    name="World",
    style_function=style_fn,
    highlight_function=highlight_fn,
    tooltip=folium.features.GeoJsonTooltip(
        # Diese Datei nutzt 'ADMIN' → falls nötig auf ["ADMIN"] ändern
        fields=["name"],
        aliases=["Land:"],
        sticky=True
    )
).add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

# Karte speichern
m.save("map_4_flaechen_online.html")
print("Gespeichert: map_4_flaechen_online.html")