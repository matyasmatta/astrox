import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import map_coordinates_format

# Create a new map
#map = Basemap(projection='merc', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
map = Basemap(projection='robin', lon_0=0, resolution='l')

# Draw coastlines and country boundaries
map.drawcoastlines()
map.drawcountries()

# Define the coordinates
coordinates = map_coordinates_format.main()

# Convert coordinates to map projection
x, y = zip(*[map(lon, lat) for lat, lon in coordinates])

# Plot the points
map.plot(x, y, 'ro')

# Show the map
plt.show()