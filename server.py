#!/usr/bin/env python3
import flask
import shelve
import json
import RPi.GPIO as gpio
from datetime import date, timedelta
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type" 

@app.route("/", methods=["GET"])
def main():
    d = shelve.open("/home/pi/Desktop/database")
    value = d["totaal"]
    d.close()
    return {"text": str(value), "money": "€"+str(round(value*0.0085333,2)), "energy": str(round(value*0.02,2)) + " kWh", "co2": str(round(value*0.02*0.23 + 0.0003*value*0.02, 2)) + " kg CO2"}, 200, {"Access-Control-Allow-Origin": "*"}


@app.route("/last-seven-days", methods=["GET"])
def last_seven_days():
    page = flask.request.args.get('week', default=0, type=int)
    d = shelve.open("/home/pi/Desktop/database")

    thisWeekValues = [0,0,0,0,0,0,0]
    monday = date.today() - timedelta(days = date.today().weekday() + (page*7))
    for i in range(7):
        try:
            thisWeekValues[i] = d[str(monday+timedelta(days=i))]
        except:
            thisWeekValues[i] = 0
    return {
        "monday": str(thisWeekValues[0]),
        "tuesday": str(thisWeekValues[1]),
        "wednesday": str(thisWeekValues[2]),
        "thursday": str(thisWeekValues[3]),
        "friday": str(thisWeekValues[4]),
        "saturday": str(thisWeekValues[5]),
        "sunday": str(thisWeekValues[6]),
    }, 200, {"Access-Control-Allow-Origin": "*"}
    

@app.route("/timer", methods=["GET", "PUT"])
def timer():
    db = shelve.open("/home/pi/Desktop/timer")
    if flask.request.method == "PUT":
        data = json.loads(flask.request.data)
        db["showerTime"] = data["showerTime"]
        db.close()
        return ""
    if flask.request.method == "GET":
        if "showerTime" in db.keys():
            time = db.get("showerTime")
            db.close()
            return {"isSet": True, "time": time}, 200, {"Access-Control-Allow-Origin": "*"}
        else:
            db.close()
            return {"isSet": False, "time": 0}, 200, {"Access-Control-Allow-Origin": "*"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
