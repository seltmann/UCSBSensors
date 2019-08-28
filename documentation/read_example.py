
import pandas as pd
import numpy as np
import requests
from datetime import date, datetime, timedelta
from io import StringIO

from arable.client import ArableClient
from lib.physics import *

import matplotlib
import matplotlib.pyplot as plt

# Jupyter utilities, will throw an error in IDLE
#%load_ext autoreload
#%autoreload 2
#%matplotlib inline

font = {'size'   : 12}

matplotlib.rc('font', **font)

# Grab some mark data
email = 'user@loremipsum.com'
device = 'A000541' 
a = ArableClient()
a.connect(email, password='abcd1234', tenant='loremipsum')

sta = "2018-04-25 00:00:00"
end = datetime.now()
end = end.strftime("%Y-%m-%dT%H:%M:%SZ")

df = a.query(select='all', 
               format='csv', devices=[device], 
               measure="hourly", 
               order="time", 
               end=end, start=sta, 
               limit=10000) 

df = StringIO(df)
df = pd.read_csv(df, sep=',', error_bad_lines=False)

# GPS doesn't read initially
df = df[3:]

df['time'] = pd.to_datetime(df['time'])
df.index = df['time']
df['doy'] = doy_(df.index)


td = pd.to_timedelta(df.long.iloc[0]/360.*24., unit = 'h').to_pytimedelta()

df['solartime'] = df.time + td
df['solartime'] = pd.to_datetime(df['solartime'])
df.index = df['solartime']

# Some useful variables

SWP = SWpot_(df.time.dt, df.lat, df.long)

df['k'] = df.SWdw / SWP

psi = solar_psi_(df.time.dt, df.lat, df.long) # Solar Zenith Angle
cospsi = np.cos(psi)
psimax = solar_phi_(df.lat) - solar_delta_(df.time.dt, df.long)
cospsimax = cos(psimax)
df['cospsi'] = cospsi
                
df['b1r'] = df.B1uw / df.B1dw
df['b2r'] = df.B2uw / df.B2dw
df['b3r'] = df.B3uw / df.B3dw
df['b4r'] = df.B4uw / df.B4dw
df['b5r'] = df.B5uw / df.B5dw
df['b6r'] = df.B6uw / df.B6dw
df['b7r'] = df.B7uw / df.B7dw

df['alb'] = -df.SWuw / df.SWdw

# Plot using Pyplot

fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(12,12))
# Reflectances
line1, = axes[0].plot(df.index, df.b1r, color='#270dab', label = 'b1r')
line2, = axes[0].plot(df.index, df.b2r, color='#0dab86', label = 'b2r')
line3, = axes[0].plot(df.index, df.b3r, color='#a8ab0d', label = 'b3r')
line4, = axes[0].plot(df.index, df.b4r, color='#b83400', label = 'b4r')
line5, = axes[0].plot(df.index, df.b5r, color='#8e4629', label = 'b5r')
line6, = axes[0].plot(df.index, df.b6r, color='#5c5c5c', label = 'b6r')
line7, = axes[0].plot(df.index, df.b7r, color='#00c2db', label = 'b7r')
line8, = axes[0].plot(df.index, df.alb, color='#000000', label = 'alb')
#axes[0].legend(handles=[line1, line2, line3, line4, line5, line6, line7], loc=2)
axes[0].set_ylabel('Reflectance: %')
axes[0].set_ylim(0,1)
axes[0].set_xlim(np.min(df.index),np.max(df.index))


line1, = axes[1].plot(df.index, -df.B1uw/df.SWuw, color='#270dab', label = 'b1r')
line2, = axes[1].plot(df.index, -df.B2uw/df.SWuw, color='#0dab86', label = 'b2r')
line3, = axes[1].plot(df.index, -df.B3uw/df.SWuw, color='#a8ab0d', label = 'b3r')
line4, = axes[1].plot(df.index, -df.B4uw/df.SWuw, color='#b83400', label = 'b4r')
line5, = axes[1].plot(df.index, -df.B5uw/df.SWuw, color='#8e4629', label = 'b5r')
line6, = axes[1].plot(df.index, -df.B6uw/df.SWuw, color='#5c5c5c', label = 'b6r')
line7, = axes[1].plot(df.index, -df.B7uw/df.SWuw, color='#00c2db', label = 'b7r')
#line8, = axes[1].plot(df.index, df.SWuw, color='#000000', label = 'alb')
#axes[0].legend(handles=[line1, line2, line3, line4, line5, line6, line7], loc=2)
axes[1].set_ylabel('Radiance')
axes[1].set_ylim(0,0.05)
axes[1].set_xlim(np.min(df.index),np.max(df.index))


line1 = axes[2].scatter(df.index, df.k, s=14, c = df.time, label = 'SWP_filter')
line1 = axes[2].plot(df.index, df.cospsi, color='#000000', label = 'SZA_filter')
axes[2].set_ylabel('SWP and SZA')
axes[2].set_ylim(0,1)
axes[2].set_xlim(np.min(df.index),np.max(df.index))

line1, = axes[3].plot(df.index, df['SWdw'], color='#DDDDDD', label = 'SWdw')
line2, = axes[3].plot(df.index, SWP, color='#FF00BB', label = 'SWpot')
axes[3].set_ylabel('SW')
#axes[3].set_ylim(0,1)
axes[3].set_xlim(np.min(df.index),np.max(df.index))