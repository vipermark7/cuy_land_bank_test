from flask import Flask
from flask import render_template, jsonify
from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen
from decimal import Decimal
import lxml
import requests
import xmltodict
import json
from gmplot import GoogleMapPlotter as gmplotter

# Used this code to parse the xml, then put the parsed xml into a file
url = "http://neocando.case.edu/cando/housingReport/lbxml.jsp?parcel=109-02-088"
raw_url_data = requests.get(url).content
parsed_xml = Soup(raw_url_data, "lxml")

with open('parsed.xml') as p:
    doc = xmltodict.parse(p.read(), process_namespaces=True)

# parsed_json will just be used for outputting to the screen
parsed_json = json.dumps(doc, indent=4, sort_keys=True)

# data['html']['body']['lbstream']['parcelid']['source'][0]['record']['latitude']['value'] to get latitude value
parcel_data = doc['html']['body']['lbstream']['parcelid']['source'][0]['record']
lats = []
longs = []
latlongs = set()

for parcel in parcel_data:
    latitude = parcel_data['latitude']['value']
    longitude = parcel_data['longitude']['value']
    lats.append(float(latitude))
    longs.append(float(longitude))
for i in lats:
    latlongs.add(i)
for i in longs:
    latlongs.add(i)

# passing coordinates into GoogleMapsPlotter
api_key = "AIzaSyCEKNzRQsT0ztBlDvRRJsGWSjHKUnvkYgA"

map1 = gmplotter(lats[0], longs[0], zoom=14, apikey=api_key)
map2 = gmplotter(lats[1], longs[1], zoom=14, apikey=api_key)
maps = [map1, map2]
for i in maps:
    i.draw('templates/index.html')
app = Flask(__name__)


@app.route('/json')
def print_json():
    """Uses jsonify() to return the full formatted JSON document to the user"""
    return jsonify(doc)


@app.route('/')
def show_map():
    """Shows view with data from Google Maps API and relevant JSON data from the XML stream"""
    print(latlongs)
    return render_template('index.html', coords=latlongs, maps=maps)


@app.route('/latlong')
def print_lat_and_long():
    """Prints latitude and longitude data from our JSON data"""

