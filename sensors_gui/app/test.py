#!/usr/bin/env python
# coding: utf-8


# Run in python 3.7+
# Script for all sensor data

import sys
import arable
from   arable.client   import ArableClient as a
a = a()
import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from   datetime        import timedelta
from   datetime        import datetime
import pandas          as     pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from   io              import StringIO
from   sensor_includes import email, password_ccber, tenant_ccber
#import arable_data_dict as dd

# Datetime object to format "%Y-%m-%dT%H:%M:%SZ"
def dt_to_ymd_hms(x):
    return x.strftime("%Y-%m-%dT%H:%M:%SZ")
# Append "%Y-%m-%dT%H:%M:%SZ" to list
def append_ymd_hms(a, b):
    a.append(dt_to_ymd_hms(b))
# Reverse dt_to_ymd_hms
def ymd_hms_to_dt(x):
    return datetime.strptime(x, "%Y-%m-%dT%H:%M:%S")

# Datetime object to format "%Y-%m-%d"
def dt_to_ymd(x):
    return x.strftime("%Y-%m-%d")
# Reverse dt_to_ymd
def ymd_to_dt(x):
    return datetime.strptime(x, "%Y-%m-%d")

# Datetime object to format "%Y-%m"
def dt_to_ym(x):
    return x.strftime("%Y-%m")
# Append "%Y-%m" to list
def append_ym(a, b):
    try:
        a.append(dt_to_ym(b))
    except:
        a.append(dt_to_ym(ym_to_dt(b)))
# Reverse dt_to_ym
def ym_to_dt(x):
    return datetime.strptime(x, "%Y-%m")

# Append string to list
def append_string(a, b):
    a.append(str(b))
    
# Append temp lists to list
def append_temp_list(temp_list, main_list):
    main_list.append(temp_list)
    
a.connect(email = email, password = password_ccber, tenant = tenant_ccber)

dt = datetime.now()

device_ids     = [] # Ex. A00****
device_names   = [] # Ex. Lagoon Ice Plants
device_created = [] # Ex. 2019-10-10T00:00:00

# The devices of interest have Z in the Location Name on the Arable website.
# These Location Names are added to device_names.
# The corresponding Device ID is added to device_ids.
for i in a.devices():
    if i['location']['name'] != '':
        device_names.append(str(i['location']['name']))
        device_ids.append(str(i['name']))
        device_created.append(str(i['created']))

#print(['{:<7}'.format(str(i)) for i in device_ids])
#print(device_names)
#print(device_created)

# Converts each item in device_ids to a list.          
device_ids = list(map(lambda el:[el], device_ids))

def arable_query(s, b, c, d, e, f, g):
    df = a.query(select = str(s),
               format = str(b),
               devices = c,
               measure = str(d),
               order = str(e),
               end = f,
               start = g,
               limit = 100000000)
    df = StringIO(df)
    df = pd.read_csv(df, sep=',', error_bad_lines=False)
    return df

# Monthly
m_start    = []
m_start_fn = []
m_end      = []
m_end_fn   = []

# Yearly
y_start    = []
y_start_fn = []
y_end      = []
y_end_fn   = []

# All Time
astart     = []
start_fn   = []
end        = []
end_fn     = []

for j in range(len(device_created)):
    ms  = []
    msf = []
    me  = []
    mef = []
    
    ys  = []
    ysf = []
    ye  = []
    yef = []
    
    s   = []
    sf  = []
    e   = []
    ef  = []
    
    def new_month(new_m):
        append_ymd_hms(ms, new_m)
        append_string(me, new_m)
        append_ym(msf, new_m)  
        append_ym(mef, new_m)
        
    def new_year(new_y):
        append_ymd_hms(ys, new_y)
        append_string(ye, new_y)
        append_ym(ysf, new_y)
        append_ym(yef, new_y)
    
    device_created_ymd = (device_created[j])[:10]
    start              = ymd_to_dt(device_created_ymd)
    append_string(ms, start)
    append_string(ys, start)
    append_string(s, start)
    append_ym(msf, start)
    append_ym(ysf, start)
    append_ym(sf, start)
    
    start  = start.replace(day=1)
    
    if start.year == dt.year:
        for i in range(start.month+1, dt.month+1):
            new_month(start.replace(month=i))
    
    elif start.year != dt.year: 
        for i in range(dt.year-start.year):
            for j in range(start.month+1, 13): 
                new_month(start.replace(month=j))
        for i in range(start.year+1, dt.year+1):
            newyr = start.replace(year=i, month=1)
            new_year(newyr)
            for j in range(1, dt.month+1):
                new_month(newyr.replace(month=j))
    
    append_string(me, dt)
    append_string(ye, dt)
    append_string(e, dt)
    append_ym(mef, dt)
    append_ym(yef, dt)
    append_ym(ef, dt)
    
    append_temp_list(ms, m_start)
    append_temp_list(me, m_end)
    append_temp_list(msf, m_start_fn)
    append_temp_list(mef, m_end_fn)
    
    append_temp_list(ys, y_start)
    append_temp_list(ye, y_end)
    append_temp_list(ysf, y_start_fn)
    append_temp_list(yef, y_end_fn)
    
    append_temp_list(s, astart)
    append_temp_list(e, end)
    append_temp_list(sf, start_fn)
    append_temp_list(ef, end_fn)
    
# Writes a .csv file for each device.
# Hourly data is separated by month; daily data is separated by year.
# Ex. A000***_hourly_2019-01_2019-02.csv
import time
def write_csv_file(sta, end, i, sta_f, end_f, device): 
    print(str(device)[2:-2] + ' has been active since ' + str(sta[0]) + '.')
    for j in range(len(sta)):
        fn = str(device)[2:-2] + '_' + str(i) + '_' + str(sta_f[j]) + '_' + str(end_f[j]) + '.csv'
        try:
            df = a.query(select = 'all', format = 'csv', devices = device, measure = str(i), order = "time", end = end[j], start = sta[j], limit = 100000000)
            df = StringIO(df)
            df = pd.read_csv(df, sep=',', error_bad_lines=False)
            df = df.drop('location', 1)
            df.to_csv(fn, sep = ",")
            print('Successfully wrote ' + fn)
        except:
            print('Error writing ' + fn)
            continue   
def inputs(d_input, t_input, dev):
    # Writes data to a .csv file
    for d in dev:
        if 1 <= j <= int(len(device_ids)):
            i = j-1
            if t_input == 1:
                if d_input == 1:
                    write_csv_file(y_start[i], y_end[i],      "daily", y_start_fn[i], y_end_fn[i], device_ids[i])
                elif d_input == 2:
                    write_csv_file(y_start[i], y_end[i],     "hourly", y_start_fn[i], y_end_fn[i], device_ids[i])
                elif d_input == 3:
                    write_csv_file(y_start[i], y_end[i],    "aux_raw", y_start_fn[i], y_end_fn[i], device_ids[i])
                elif d_input == 4:
                    write_csv_file(y_start[i], y_end[i], "calibrated", y_start_fn[i], y_end_fn[i], device_ids[i])
            if t_input == 2:
                if d_input == 1:
                    write_csv_file(m_start[i], m_end[i],      "daily", m_start_fn[i], m_end_fn[i], device_ids[i])
                elif d_input == 2:
                    write_csv_file(m_start[i], m_end[i],     "hourly", m_start_fn[i], m_end_fn[i], device_ids[i])
                elif d_input == 3:
                    write_csv_file(m_start[i], m_end[i],    "aux_raw", m_start_fn[i], m_end_fn[i], device_ids[i])
                elif d_input == 4:
                    write_csv_file(m_start[i], m_end[i], "calibrated", m_start_fn[i], m_end_fn[i], device_ids[i])
            if t_input == 3:
                if d_input == 1:
                    write_csv_file(astart[i], end[i],      "daily", start_fn[i], end_fn[i], device_ids[i])
                elif d_input == 2:
                    write_csv_file(astart[i], end[i],     "hourly", start_fn[i], end_fn[i], device_ids[i])
                elif d_input == 3:
                    write_csv_file(astart[i], end[i],    "aux_raw", start_fn[i], end_fn[i], device_ids[i])
                elif d_input == 4:
                    write_csv_file(astart[i], end[i], "calibrated", start_fn[i], end_fn[i], device_ids[i])
   return 'Wrote files' 
