#!/usr/bin/env python3
# *-* coding:utf-8 *-*

"""

:mod:`lab_flask` -- serving up REST
=========================================

LAB_FLASK Learning Objective: Learn to serve RESTful APIs using the Flask
library
::

 a. Using Flask create a simple server that serves the following string for the
    root route ('/'):
    "<h1>Welcome to my server</h1>"

 b. Add a route for "/now" that returns the current date and time in string
    format.

 c. Add a route that converts Fahrenheit to Centigrade and accepts the value to
    convert in the url.  For instance, /fahrenheit/32.0 should return "0.0"

 d. Add a route that converts Centigrade to Fahrenheit and accepts the value to
    convert in the url.  For instance, /centigrade/0.0 should return "32.0"

"""
from flask import Flask, request
import datetime
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == "GET":
        return "<h1>Welcome to my server</h1>"
    elif request.method == "POST":
        data = json.loads([i for i in request.form.keys()][0])
        if "hello" in data:
            return str("Your hello string is: " + str(data["hello"] + "\n"))
        else:
            data = str("Must have hello string in request!!")
            return data, 406
        date = datetime.datetime.now()
        return str(date.strftime("%Y-%m-%d %H:%M:%S") + "\n")


@app.route('/now')
def current_date():
    date = datetime.datetime.now()
    return str(date.strftime("%Y-%m-%d %H:%M:%S") + "\n")


@app.route('/fahrenheit/<temp>')
# @app.route('/fahrenheit/<int:temp>')
def FtoC(temp):
    try:
        temp = float(temp)
        c_tmp = (temp - 32) * 5/9
        return str("The temperature in Celcius is: " + str(c_tmp) + "\n")
    except Exception as e:
        return str(str(e) + "\n")


@app.route('/centigrade/<temp>')
# @app.route('/centigrade/<int:temp>')
def CtoF(temp):
    try:
        temp = float(temp)
        f_tmp = (temp * 9/5) + 32
        return str("The temperature in Fahrenheit is: " + str(f_tmp) + "\n")
    except Exception as e:
        return str(str(e) + "\n")


if __name__ == "__main__":
    app.run()
