from flask import Flask
from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen
from decimal import Decimal
import lxml, requests, xmltodict, json

# Used this code to parse the xml, then put the parsed xml into a file
url = "http://neocando.case.edu/cando/housingReport/lbxml.jsp?parcel=109-02-088"
raw_url_data = requests.get(url).content
parsed_xml = Soup(raw_url_data, "lxml")

with open('parsed.xml') as p:
    doc = xmltodict.parse(p.read(), process_namespaces=True)

#parsed_json will just be used for outputting to the screen
parsed_json = json.dumps(doc, indent=4, sort_keys=True)



with open("parsed.json") as f:
    data = json.load(f)

# data['html']['body']['lbstream']['parcelid']['source'][0]['record']['latitude']['value'] to get latitude value
parcel_data = data['html']['body']['lbstream']['parcelid']['source'][0]
lats = []
longs = []
for parcel in parcel_data:
    latitude = Decimal(parcel_data['record']['latitude']['value'])
    longitude = Decimal(parcel_data['record']['longitude']['value'])
    lats.append(str(latitude))
    longs.append(str(longitude))

app = Flask(__name__)
@app.route('/')
def print_json():
    return parsed_json

@app.route('/latlong')
def print_lat_and_long():
    latlongs = ""
    for i in lats:
        latlongs += " " + i
    for i in longs:
        latlongs += " " + i

    return latlongs         

