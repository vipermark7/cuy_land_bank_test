from flask import Flask
from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen
import lxml, requests, xmltodict, json, pprint

# Used this code to parse the xml, then put the parsed xml into a file
url = "http://neocando.case.edu/cando/housingReport/lbxml.jsp?parcel=109-02-088"
raw_url_data = requests.get(url).content
parsed_xml = Soup(raw_url_data, "lxml")

with open('parsed.xml') as p:
    doc = xmltodict.parse(p.read(), process_namespaces=True)

parsed_json = json.dumps(doc, indent=4, sort_keys=True)


app = Flask(__name__)
@app.route('/')
def print_json():
    return parsed_json

