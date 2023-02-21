import api


def get_altitude(coordinates_latitude, coordinates_longtitude, year, month, day, hour, minute, second):
    # use the NASA API to be able to calculate sun's position
    ts = api.load.timescale()
    ephem = api.load("ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/de421.bsp")

    # define sky objects
    sun = ephem["Sun"]
    earth = ephem["Earth"]

    # define where photo was taken(usually via EXIF data)
    # given coordinates calculate the altitude (how many degrees sun is above the horizon), additional data is redundant
    location = api.Topos(coordinates_latitude, coordinates_longtitude, elevation_m=500)
    sun_pos = (earth + location).at(ts.tt(year,month,day,hour,minute,second)).observe(sun).apparent()
    altitude, azimuth, distance = sun_pos.altaz()

    # print(f"Azimuth: {azimuth.degrees:.4f}")
    # print(f"Altitude: {altitude.degrees:.4f}")

    altitude= float(altitude.degrees)
    return(altitude)

def get_azimuth(coordinates_latitude, coordinates_longtitude, year, month, day, hour, minute, second):
    # use the NASA API to be able to calculate sun's position
    ts = api.load.timescale()
    ephem = api.load("ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/de421.bsp")

    # define sky objects
    sun = ephem["Sun"]
    earth = ephem["Earth"]

    # define where photo was taken(usually via EXIF data)
    # given coordinates calculate the altitude (how many degrees sun is above the horizon), additional data is redundant
    location = api.Topos(coordinates_latitude, coordinates_longtitude, elevation_m=500)
    sun_pos = (earth + location).at(ts.tt(year,month,day,hour,minute,second)).observe(sun).apparent()
    altitude, azimuth, distance = sun_pos.altaz()

    # print(f"Azimuth: {azimuth.degrees:.4f}")
    # print(f"Altitude: {altitude.degrees:.4f}")

    azimuth= float(azimuth.degrees)
    return(azimuth)

def starting_point_corrector(x_centre, y_centre, x_increase_final, y_increase_final):
    constant_for_starting_point_correction = 10
    x_final = x_centre - constant_for_starting_point_correction*x_increase_final
    y_final = y_centre - constant_for_starting_point_correction*y_increase_final
    x_final = round(x_final, 0)
    x_final = int(x_final)
    y_final = round(y_final, 0)
    y_final = int(y_final)
    return x_final, y_final
    
def calculate_angle_for_shadow(north, latitude, longitude, year, month, day, hour=0, minute=0, second=0):
    azimuth = get_azimuth(latitude, longitude, year, month, day, hour, minute, second)
    print(north, azimuth)
    total_angle = north + azimuth - 180
    while total_angle >= 360:
        total_angle -= 360
    print(total_angle)
    return total_angle

calculate_angle_for_shadow(140, -28.29959, 31.91066, 2022, 1, 15, 4, 49, 0)