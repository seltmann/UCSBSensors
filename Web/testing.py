#!flask/bin/python

import sys

from flask import Flask, render_template, request, redirect, Response, jsonify
import random, json

from search import main, find_top_folder, find_file
from googleapiclient.http import MediaIoBaseDownload
import io
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', "OPTIONS"])
def index():
    return render_template('index.html')


@app.route('/test', methods=['GET', 'POST', "OPTIONS"])
def test():
    urll = []
    if request.method == 'POST':
        question = request.get_json()
        # print(question["Site"])
        site = question["Site"]
        # habitat = question["Habitat"]
        year = question["Year"]
        data_type = question["DataType"]
        # folder = "Arable_Data"
        service = main()
        folder_id = find_top_folder(service, "Arable_Data")
        # print(folder_id)
        fn = find_file(service, site, year, data_type)
        # print(fn)
        for match in fn.keys():
            url = fn[match]["Link"]
            # print(url)
            url_avoid_cors = {"URL": str(url)}  # f"https://cors-anywhere.herokuapp.com/{url}"}
            urll.append(url_avoid_cors)
            return url_avoid_cors
        # return redirect(f"https://cors-anywhere.herokuapp.com/{url}", code = 302)
        return ""

    elif request.method == 'GET':
        url_avoid_cors = urll[0]
        return url_avoid_cors


app.run(server_host="0.0.0.0", host="0.0.0.0", port=5000)

