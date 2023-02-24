import numpy as np
from datetime import datetime
alpha = 1.81833734228
n = 10000000

t = datetime.now()
for i in range(n):
    alpha = alpha * 180 / np.pi
    alpha = alpha * np.pi / 180
    if i == 1/4*n or i == 1/2*n or i == 3/4*n or i == n-1:
        print(alpha)
print("second:", datetime.now() - t)

t = datetime.now()
for i in range(n):
    alpha = alpha * 57.29577951
    alpha = alpha / 57.29577951
    if i == 1/4*n or i == 1/2*n or i == 3/4*n or i == n-1:
        print(alpha)
print("third:", datetime.now() - t)

eda = []

while True or abs(eda[-1]-eda[-2]<1):
    print(1)