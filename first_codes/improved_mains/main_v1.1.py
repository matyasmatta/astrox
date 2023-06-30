import stiny_maty
import sever_eda

data = stiny_maty.sun_data.altitude("34.28614 S", "147.9849 E", 2022, 1, 15, 5, 16, 50)
print(data)

data = stiny_maty.calculate_shadow('.\\zchop.meta.x000.y000.n011.jpg', 294,199,310)
print(data)

data, coefficient = sever_eda.find_north(".\\namibie1.jpg", ".\\namibie2.jpg", "-25.07194", "-25.49306")
print(data)