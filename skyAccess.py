'''
This code plots the sky visibility in declination and hour angle for a
given telescope and observation time (here is the JKT telescope).
The contours show the accesible coordinates with constant zenith angles.

December 2018 - Azar 1397
farhang@nailydata.com
'''

import numpy as np
import matplotlib.pyplot as plt

from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle
from astropy.time import Time

# JKT telescope coordinates
lon = 17.878 # longitude in degree
lat = 28.761 # latitude in degree
h = 2364 # height in meter

jkt = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=h*u.m)
obsTime = Time('2018-01-20 20:00:00') #  observation time

# Local sidereal time will be needed to compute the hour angle
sidTime = obsTime.sidereal_time('mean', longitude=lon)
print 'Mean local sidereal time: ', sidTime

angTresh = Angle('6h0m0s') # a threshold angle for plotting purposes
angPeriod = Angle('-24h0m0s') # hour angle period

N = 180 # discretization angle step
# considering the constant zwnith angles eqZenith (cosntant alttitudes)
for eqZenith in range(10,90,10):
    alt = []
    [alt.append(eqZenith) for i in range(N)]
    az = np.linspace(0,360,N) # includong all possible azimuth angles
    # convering all AltAz angles to equatorial coordinates (icrs)
    obj = SkyCoord(az, alt, unit='deg', frame='altaz', location=jkt, obstime=obsTime).transform_to('icrs')
    ha =  sidTime - obj.ra # hour angle

    ind=np.where(ha>=angTresh)
    ha[ind] = angPeriod+ha[ind]

    plt.plot(ha,obj.dec)

plt.xlim(left=-18, right=6)
plt.ylim(bottom=-60, top=90)
plt.title('JKT visibility plot')
plt.xlabel('Hour angle')
plt.ylabel('Dec')
plt.show()
