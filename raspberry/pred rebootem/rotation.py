from sense_hat import SenseHat

sense = SenseHat()

red = (255, 0, 0)

while True:
    o = sense.get_orientation_degrees()
    p = o['pitch']
    r = o['roll']
    y = o['yaw']

    print(round(y,3))

    o = sense.get_orientation_radians()
    p = o['pitch']
    r = o['roll']
    y = o['yaw']

    print(round(y,3))


    for event in sense.stick.get_events():
        if  event.action == "pressed":
            print("necolasfjksdklůfjlsdfjlkasdjfl")




    
    