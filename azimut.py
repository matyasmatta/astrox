from skyfield import api
from skyfield import almanac
      
ts = api.load.timescale()
ephem = api.load_file("de421.bsp")

sun = ephem["Sun"]
earth = ephem["Earth"]

location = api.Topos("49.73880 N", "13.39350 E", elevation_m=500)
sun_pos = (earth + location).at(ts.now()).observe(sun).apparent()
altitude, azimuth, distance = sun_pos.altaz()

print(f"Azimuth: {azimuth.degrees:.4f}")
print(f"Altitude: {altitude.degrees:.4f}")
print("distance:", distance)
