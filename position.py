from skyfield.api import load, wgs84, EarthSatellite
ts = load.timescale()
stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
satellites = load.tle_file(stations_url)
by_name = {sat.name: sat for sat in satellites}
satellite = by_name['ISS (ZARYA)']
#print(satellite)
t = ts.now()
geocentric = satellite.at(t)
#print(geocentric.position.km)
lat, lon = wgs84.latlon_of(geocentric)
print('Latitude:', lat)
print('Longitude:', lon)
#print(t.ut1)
#print(t)
