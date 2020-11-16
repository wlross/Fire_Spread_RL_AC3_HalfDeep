import numpy as np
import random

start = 1
decay = .98

for i in range(1,100):
    print(random.uniform(0,1))
    print(start*(decay**i))