import math as magic
import numpy as np

def servicio():
    random = magic.ceil(np.random.normal(5.77,2.11075,1))
    if random < 5:
        random = 5
    return random