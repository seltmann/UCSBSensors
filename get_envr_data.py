#!/usr/bin/env python
# Script for all sensor data

import sys
import os

import schedule
import time
    
def job():
    print("I am doing this job!")
    #os.system('runipy get_sensor_data.ipynb')
    os.system('runipy make_csv_files.ipynb')

schedule.every().day.at("9:40").do(
job)

while True:
    schedule.run_pending()
    time.sleep(1)

