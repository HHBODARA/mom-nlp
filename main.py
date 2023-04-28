import os
from datetime import date, datetime
import time
import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort


app = Flask(__name__)

def get_data():
  f = open('sample.json')
  json_data = json.load(f)

  return json_data





@app.route("/")
def main():
  json_data1 = get_data()
  return render_template("index.html",json_data=json_data1)


app.run(debug = True, threaded=True, host='0.0.0.0', port=5001)