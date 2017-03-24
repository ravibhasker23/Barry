#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import re

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "barry.robot":
        return {}
    
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    data = yql_query
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    tech = parameters.get("searchTech")
    if tech is None:
        return None
    
    #Loc = parameters.get("searchLoc")
    #if Loc is None:
        #return None
        
    return tech


def makeWebhookResult(data):
    
    result = data.get("result")
    parameters = result.get("parameters")
    tech = parameters.get("searchTech")
    resource = {'JAVA':100, 'C++':200, '.Net':300}
    # print(json.dumps(item, indent=4))

    speech = "Technology: " + tech + "Resources " + str(resource[tech])
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "Barry"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
