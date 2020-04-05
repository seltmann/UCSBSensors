#!/usr/bin/env python
# Script for all sensor data

import sys
import os

import schedule
import time

import smtplib
 
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s
' % from_addr
    header += 'To: %s
' % ','.join(to_addr_list)
    header += 'Cc: %s
' % ','.join(cc_addr_list)
    header += 'Subject: %s

' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    
def job():
    print("I am doing this job!")
    os.system('runipy get_sensor_data.ipynb')
    os.system('runipy make_csv_files.ipynb')
    sendemail(from_addr    = 'macgregor@ucsb.edu', 
          to_addr_list = ['macgregor@ucsb.edu'],
          cc_addr_list = ['macgregor@ucsb.edu'], 
          subject      = 'CCBER Arables', 
          message      = 'The code ran!', 
          login        = 'macgregor@ucsb.edu', 
          password     = 'XXXXX')


schedule.every().day.at("10:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

