#how does the temperature change while Raspberry calculates the second power
#works on Raspberry

#by Eda

from sense_hat import SenseHat
from gpiozero import CPUTemperature
import matplotlib.pyplot as plt
from time import sleep

sense = SenseHat()
cpu = CPUTemperature()

x=2
st, ct = [], []
for i in range(20):
    x=x*x
    print(i, "+", x)
    st.append(sense.temperature)
    ct.append(cpu.temperature)
    sleep(0)

plt.plot(st)
plt.plot(ct)
plt.legend(['Sense HAT temperature sensor', 'Raspberry Pi CPU temperature'], loc='center')
plt.show()