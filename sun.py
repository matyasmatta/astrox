from skyfield import api
from skyfield.api import load

# use the NASA API to be able to calculate sun's position
ts = api.load.timescale()
ephem = api.load("ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/de421.bsp")

# define sky objects
sun = ephem["Sun"]
earth = ephem["Earth"]

coordinates_latitude = "18.5 N"
coordinates_longtitude = "55.5 E"
year,month,day,hour,minute,second = 2023,4,25,8,25,24 

# given coordinates calculate the altitude (how many degrees sun is above the horizon), additional data is redundant
location = api.Topos(coordinates_latitude, coordinates_longtitude, elevation_m=500)
sun_pos = (earth + location).at(ts.tt(year,month,day,hour,minute,second)).observe(sun).apparent()
altitude, azimuth, distance = sun_pos.altaz()
azimuth= float(azimuth.degrees)
print(azimuth)