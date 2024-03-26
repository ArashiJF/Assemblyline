from cola import *

class Params:
    def __init__(self,arrival,leaving,delay,servicio,numero):
        self.arrival = arrival
        self.leaving = leaving
        self.delay = delay
        self.servicio = servicio
        self.fila = Cola()
        self.fila.enqueue(numero)
        self.fila.dequeue()

    def get(self):
        return self.arrival, self.leaving, self.delay, self.servicio, self.fila