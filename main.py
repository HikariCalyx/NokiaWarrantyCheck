#!/usr/bin/python3
from flask import Flask, request, abort
from gevent import pywsgi
from warranty_api import warranty
import datetime

# Configurations
auth_port = 443

app = Flask(__name__)
app.register_blueprint(warranty)

@app.route('/', methods=['GET'])
def index():
    return("""OK""")

print("API Server\n")
server = pywsgi.WSGIServer(('0.0.0.0', auth_port), app, certfile='/etc/letsencrypt/live/api.yourdomain.com/fullchain.pem', keyfile='/etc/letsencrypt/live/api.yourdomain.com/privkey.pem')
print("Now listening on Port " + str(auth_port))
server.serve_forever()
