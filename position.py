from orbit import ISS
from skyfield.api import load
t = load.timescale().now()
position = ISS.at(t)
time = t
location = position.subpoint()
print(location)
print(time)
print(f'Elevation: {location.elevation.km}')