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
# commenting this code out as it changes the html file every time it runs
#api_key = "AIzaSyDjF1arEQu74T0GWqcBbKO8gGhYTNIC6F8"

#map1 = gmplotter(lats[0], longs[0], zoom=14, apikey=api_key)
#map2 = gmplotter(lats[1], longs[1], zoom=14, apikey=api_key)
#maps = [map1, map2]
#for i in maps:
#    i.draw('templates/index.html')
app = Flask(__name__)


@app.route('/json')
def print_json():
    """Uses jsonify() to return the parcel data in JSON to the user"""
    return jsonify(parcel_data)


@app.route('/')
def show_map():
    """Shows view with data from Google Maps API and relevant JSON data from the XML stream"""
    print(latlongs)
    return render_template('index.html', coords=latlongs, parceldata=parcel_data)
