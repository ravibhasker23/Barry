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
    #yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    data = yql_query
    
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")  
    technology = parameters.get("searchTech")
        if technology is None:
        return None
    
   # location = parameters.get("searchLoc")
    #   if location is None:
    #    return None
    
    #role = parameters.get("searchdesignation")
    #    if role is None:
    #    return None
    
    return technology 
#+ "-" + location + "-" + role


def makeWebhookResult(data):
    
    resource = {'JAVA':100, '.Net':200, 'C#':300}
    # print(json.dumps(item, indent=4))
    
    speech = "Tech: " + Tech + "resources " + str(resource[data])

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
