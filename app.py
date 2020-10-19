from flask import Flask
from flask import render_template, jsonify
from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen
from decimal import Decimal
import lxml
import requests
import xmltodict
import json

# Used this code to parse the xml, then put the parsed xml into a file
url = "http://neocando.case.edu/cando/housingReport/lbxml.jsp?parcel=109-02-088"
raw_url_data = requests.get(url).content
parsed_xml = Soup(raw_url_data, "lxml")

with open('parsed.xml') as p:
    doc = xmltodict.parse(p.read(), process_namespaces=True)

# parsed_json will just be used for outputting to the screen
parsed_json = json.dumps(doc, indent=4, sort_keys=True)

# data['html']['body']['lbstream']['parcelid']['source'][0]['record']['latitude']['value'] to get latitude value
parcel_data = doc['html']['body']['lbstream']['parcelid']['source'][0]
lats = set()
longs = set()

for parcel in parcel_data:
    latitude = Decimal(parcel_data['record']['latitude']['value'])
    longitude = Decimal(parcel_data['record']['longitude']['value'])
    lats.add(str(latitude))
    longs.add(str(longitude))

app = Flask(__name__)


@app.route('/json')
def print_json():
    """Uses jsonify() to return formatted JSON to the user"""
    return jsonify(doc)


@app.route('/')
def show_map():
    """Shows view with data from Google Maps API and relevant JSON data from the XML stream"""
    return render_template('index.html', data=jsonify(parcel_data) )


@app.route('/latlong')
def print_lat_and_long():
    """Prints latitude and longitude data from our JSON data"""
    latlongs = ""
    for i in lats:
        latlongs += " " + i
    for i in longs:
        latlongs += " " + i

    return latlongs
