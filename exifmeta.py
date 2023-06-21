from PIL import Image, ImageStat
from exif import Image as exify
from datetime import timedelta, datetime
from skyfield import api
from skyfield.api import load

# this is a small class containing a method for date extraction that is not via the EXIF library but the PIL library
def find_time(image_path):
    img = Image.open(image_path)
    img_exif_dict = img.getexif()
    date = str(img_exif_dict[306])
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    hour = int(date[11:13])
    minute = int(date[14:16])
    second = int(date[17:19])
    return year, month, day, hour, minute, second

def pillow_ext(path):
    image = Image.open(path)
    exif = image.info['exif']
    return exif

def exify_ext(path):
    img = exify(path)
    return img

def get_latitude(image):
    with open(image, 'rb') as image_file:
        img = exify(image_file)
        try:
            latitude = img.get("gps_latitude")
            latitude_ref = img.get("gps_latitude_ref")
            if latitude == None:
                latitude, latitude_ref = (0.0, 0.0, 0.0), "A"
        except AttributeError:
            latitude, latitude_ref = (0.0, 0.0, 0.0), "A"
    decimal_degrees = latitude[0] + latitude[1] / 60 + latitude[2] / 3600
    latitude_formatted = str(str(decimal_degrees)+" "+str(latitude_ref))
    return latitude_formatted

def get_longitude(image):
    with open(image, 'rb') as image_file:
        img = exify(image_file)
        try:
            longitude = img.get("gps_longitude")
            longitude_ref = img.get("gps_longitude_ref")
            if longitude == None:
                longitude, longitude_ref = (0.0, 0.0, 0.0), "A"
        except AttributeError:
            longitude, longitude_ref = (0.0, 0.0, 0.0), "A"
    decimal_degrees = longitude[0] + longitude[1] / 60 + longitude[2] / 3600
    longitude_formatted = str(str(decimal_degrees)+" "+longitude_ref)
    return longitude_formatted 

class sun_data:
    def altitude(coordinates_latitude, coordinates_longtitude, year, month, day, hour, minute, second):
        # use the NASA API to be able to calculate sun's position
        ts = api.load.timescale()
        ephem = api.load("ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/de421.bsp")

        # define sky objects
        sun = ephem["Sun"]
        earth = ephem["Earth"]

        # given coordinates calculate the altitude (how many degrees sun is above the horizon), additional data is redundant
        location = api.Topos(coordinates_latitude, coordinates_longtitude, elevation_m=500)
        sun_pos = (earth + location).at(ts.tt(year,month,day,hour,minute,second)).observe(sun).apparent()
        altitude, azimuth, distance = sun_pos.altaz()
        altitude= float(altitude.degrees)
        return(altitude)
    def azimuth(coordinates_latitude, coordinates_longtitude, year, month, day, hour, minute, second):
        # use the NASA API to be able to calculate sun's position
        ts = api.load.timescale()
        ephem = api.load("ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/de421.bsp")

        # define sky objects
        sun = ephem["Sun"]
        earth = ephem["Earth"]

        # given coordinates calculate the altitude (how many degrees sun is above the horizon), additional data is redundant
        location = api.Topos(coordinates_latitude, coordinates_longtitude, elevation_m=500)
        sun_pos = (earth + location).at(ts.tt(year,month,day,hour,minute,second)).observe(sun).apparent()
        altitude, azimuth, distance = sun_pos.altaz()
        azimuth= float(azimuth.degrees)
        return(azimuth)