from flask import Flask, make_response, request
import sys
import time
import pytz
import json
from datetime import datetime
import paho.mqtt.publish as publish

app = Flask(__name__)

# alive test
@app.route('/')
def hello_world():
    resp = make_response("Hello: current time is [UTC %s]" %
                         datetime.utcnow().isoformat())
    resp.headers['server'] = "strange server"
    return resp

# actoboard forward data to this route
@app.route('/auto/sigfox/actoboard/update', methods = ['POST'])
def actoboard_data():
    # mandatory form data
    heads = {'device' : request.form['device'],
             'signal' : request.form['signal'],
             'data' : request.form['data'],
             'time' : request.form['time']}
    # slots in form data
    slots = {}
    for item in request.form:
        if item.startswith("slot_"):
            slots[item[5:]] = request.form[item]
    # format a time_iso string
    time_iso = datetime.fromtimestamp(float(heads['time']),
                                      tz=pytz.utc).isoformat()
    # jsons = dict heads + dict slots + time_iso
    jsons = heads.copy()
    jsons['time_iso'] = time_iso
    jsons.update(slots)
    # to MQTT
    start_path = "sigfox/actoboard/modems/%s/" % heads['device']
    msgs = [{'topic': start_path+"signal", 'payload': heads['signal'],
             'retain': True},
            {'topic': start_path+"time", 'payload': heads['time'],
             'retain': True},
            {'topic': start_path+"time_iso", 'payload': time_iso,
             'retain': True},
            {'topic': start_path+"data", 'payload': heads['data'],
             'retain': True},
            {'topic': start_path+"json", 'payload': json.dumps(jsons),
             'retain': True}]
    # add slots to msgs
    for item in slots:
        msgs.append({'topic': start_path+"slots/%s" % item,
                     'payload': slots[item], 'retain': True})
    publish.multiple(msgs, hostname="mosquitto")
    return "ok"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
