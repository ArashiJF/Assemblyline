from params import *
from cola import *
from calculoservicio import *
from Subestacion import *

"""Los datos de servicio se ajustan a una distribucion normal por tanto se usara numpy para calcular 
esos valores en ejecucion, media = 5.77, desviacion estandar = 2.11075"""

"""Esta distribucion fue encontrada a partir de un set de datos que esta adjuntado con el proyecto,
se dijo que los tiempos de servicio en cada estacion estan alrededor de los 5 y 9 minutos"""

"""Al menos 2 estaciones en la linea corresponden al horno y pintado, y ambas toman 35 minutos,
por tanto habran 2 estaciones con un tiempo de servicio fijo de 35 minutos, para razones de este proyecto
diremos que dichas estaciones son la estacion 15 y la estacion 30, y pondremos un maximo de 75 estaciones,
dicho valor puede ser cambiado en cualquier momento alterando el range en el for en la seccion donde se inicializan
las estaciones"""

"""Consideramos que entre estacion y estacion son 2 minutos para llegar"""


def main():
    """Elija cuantos carros desea ensamblar en la ejecucion, cambiando el valor de ncarros"""
    ncarros = 20
    nestaciones = 75
    nestaciones += 1
    mainfila = Cola()
    matrix = [[0 for x in range(nestaciones)] for y in range(ncarros)]

    subestacion1 = subestacion(0,0,True,True)

    """mainfila puede tomarse como el dispatcher del inicio, este es el que inicializa los carros en la
    linea de ensamblaje"""
    for i in range(ncarros):
        mainfila.enqueue(1)

    """Se inicializaran las estaciones, """

    """Se deja un inicio en la fila para el algoritmo"""

    for i in range(ncarros):
        for j in range(nestaciones):
            """En la estacion 15 y 30 los tiempos de servicio son 35"""
            if (j == 16 or j == 17 or j == 31):
                """Cada posicion en la matriz es una instancia de la clase Params, esto con el fin
                de poder guardar los tiempos de llegada, servicio y salida de cada carro en cada estacion"""
                aux1 = Params(0, 0, 0, 35, 0)
                matrix[i][j] = aux1

            else:
                servicetime = servicio()
                aux = Params(0, 0, 0, servicetime, 0)
                matrix[i][j] = aux


    """Variables que controlan la ejecucion de la simulacion"""
    #tiempo se encarga de guardar el tiempo total de cada carro en la linea
    tiempo = 0.0

    #inicio se encarga de controlar cuando es la primera vez que entra un carro en la linea
    inicio = True

    #done esta pendiente de si quedan carros por atender en la linea
    done = False

    #indice de entrada se encarga de saber que carro esta entrando en la linea
    indicesentrada = 0

    """While principal, este controla los carros que llegan"""
    while (True):

        """Mientras queden carros en el dispatcher (mainfila) este sigue agregandolos a la linea de produccion"""
        if mainfila.isEmpty() == False:
            entra = mainfila.dequeue()
            print("Entra un auto al ensamblaje")

            matrix[indicesentrada][1].fila.enqueue(entra)
            indicesentrada = indicesentrada + 1


        while (True):
            """En estas variable se guardan las posiciones de los carros en la linea de ensamblaje"""

            posicionesfila = []
            posicionescolumna = []
            for i in range(ncarros):
                for j in range(nestaciones):
                    if(matrix[i][j].fila.isEmpty() == False):
                        posicionesfila.append(i)
                        posicionescolumna.append(j)

            if len(posicionescolumna) < 1:
                done = True

            """El inicio de la simulacion, al salir, pasa el primer carro a la estacion 2 y pone la variable inicio
            en falso"""
            if (inicio == True and matrix[0][1].fila.isEmpty() == False):

                matrix[0][1].leaving = matrix[0][1].servicio

                matrix[0][2].arrival = matrix[0][1].leaving + 2

                pasa = matrix[0][1].fila.dequeue()

                matrix[0][2].fila.enqueue(pasa)

                inicio = False
                break


            """Iteramos en dichas posiciones para que toda la linea se mueva"""

            carros = Cola()
            estaciones = Cola()
            """Debido a que se usa una cola, al guardar las posiciones estas quedan invertidas
            por tanto se crean 2 variables tambien de la clase cola que se encarguen de guardarlas
            en el orden correcto"""
            carrosinvertido = Cola()
            estacionesinvertido = Cola()

            for n in posicionesfila:
                carros.enqueue(n)

            for n in posicionescolumna:
                estaciones.enqueue(n)

            while carros.isEmpty() == False:
                carrosinvertido.enqueue(carros.dequeue())

            while estaciones.isEmpty() == False:
                estacionesinvertido.enqueue(estaciones.dequeue())
            lookhere = 0

            """Este ciclo while se encarga de tomar cada posicion donde haya un carro en las estaciones
            y hacer los calculos correspondientes en la matriz, basicamente, se tiene la posicion donde
            esta cada carro en cada momento de la simulacion"""
            print(posicionesfila, posicionescolumna)
            while(True):
                if (carrosinvertido.isEmpty() == True and estacionesinvertido.isEmpty() == True):
                    break
                i = carrosinvertido.dequeue()
                j = estacionesinvertido.dequeue()


                """Las operaciones a continuacion utilizan el algoritmo entregado en la misma clase, solo que esta
                vez, ya que los carros basicamente dependen del carro que esta enfrente de ellos para saber si
                pueden o no continuar avanzando, entonces lo que se hace es que para el carro que va al frente
                este se mueve de forma normal y solo toma en cuenta su propio tiempo de salida para calcular su arrival
                en la siguiente posicion"""

                """Pero los carros que estan detras de este, lo que hacen es: Para saber su arrival en la siguiente
                estacion y si tienen que esperar o no, comparan los tiempos de salida del carro que va enfrente y 
                hacen las operaciones correspondientes para calcular el delay"""

                """Los carros van "moviendose" en la matriz hasta que al final estos abandonan la linea, este
                comportamiento se logra teniendo de que cada posicion en la matriz tiene un parametro que es
                una instancia de la clase Cola(), esta permite simular que un carro reside en ese sitio
                en determinada iteracion, y con ello puede comportarse de la manera en que se comportaria 
                un carro en una linea, este llega a una estacion, es atendido, sale de esta y es asignado 
                a la siguiente"""
                if j < nestaciones-1:
                    if j == 15:
                        if i < 1:
                            if matrix[i][j].arrival < matrix[i][j - 1].leaving:
                                matrix[i][j].delay = matrix[i][j - 1].leaving - matrix[i][j].arrival
                            else:
                                matrix[i][j].delay = 0
                            matrix[i][j].leaving = matrix[i][j].arrival + matrix[i][j].delay + matrix[i][j].servicio

                            matrix[i][j + 1].arrival = matrix[i][j].leaving + 2

                            subestacion1.libre1 = False

                            pasa = matrix[i][j].fila.dequeue()
                            matrix[i][j + 1].fila.enqueue(pasa)

                        else:
                            if matrix[i][j].arrival < matrix[i - 1][j].leaving:
                                matrix[i][j].delay = matrix[i - 1][j].leaving - matrix[i][j].arrival
                            else:
                                matrix[i][j].delay = 0
                            matrix[i][j].leaving = matrix[i][j].arrival + matrix[i][j].delay + matrix[i][j].servicio

                            if subestacion1.libre1 == False and subestacion1.libre2 == False:
                                subestacion1.libre1 = True
                                subestacion1.libre2 = True

                            if subestacion1.libre1 == True:
                                pasa = matrix[i][j].fila.dequeue()
                                matrix[i][16].arrival = matrix[i][j].leaving + 2
                                subestacion1.libre1 = False
                                matrix[i][16].fila.enqueue(pasa)

                            elif subestacion1.libre2 == True:
                                pasa = matrix[i][j].fila.dequeue()
                                matrix[i][17].arrival = matrix[i][j].leaving + 2
                                subestacion1.libre2 = False
                                matrix[i][17].fila.enqueue(pasa)
                        break
                    """Si es el carro que va en frente, este solo toma en cuenta su propio tiempo de salida para saber su arrival en la siguiente estacion"""

                    if i < 1:
                        if j == 16:
                            lookhere = j
                            if matrix[i][j].arrival < matrix[i][j - 1].leaving:
                                matrix[i][j].delay = matrix[i][j - 1].leaving - matrix[i][j].arrival
                            else:
                                matrix[i][j].delay = 0
                            matrix[i][j].leaving = matrix[i][j].arrival + matrix[i][j].delay + matrix[i][j].servicio
                            matrix[i][18].arrival = matrix[i][j].leaving + 2

                            """se desasigna el carro a la estacion actual y se asigna a la estacion siguiente"""
                            subestacion1.libre1 = True
                            subestacion1.ultimo1 = i
                            pasa = matrix[i][j].fila.dequeue()
                            matrix[i][18].fila.enqueue(pasa)

                        elif j == 18:

                            if matrix[i][j].arrival < matrix[i][16].leaving:
                                matrix[i][j].delay = matrix[i][16].leaving - matrix[i][j].arrival
                            else:
                                matrix[i][j].delay = 0
                            matrix[i][j].leaving = matrix[i][j].arrival + matrix[i][j].delay + matrix[i][j].servicio
                            matrix[i][j + 1].arrival = matrix[i][j].leaving + 2

                            pasa = matrix[i][j].fila.dequeue()
                            matrix[i][j + 1].fila.enqueue(pasa)

                        else:
                            if matrix[i][j].arrival < matrix[i][j - 1].leaving:
                                matrix[i][j].delay = matrix[i][j - 1].leaving - matrix[i][j].arrival
                            else:
                                matrix[i][j].delay = 0

                            matrix[i][j].leaving = matrix[i][j].arrival + matrix[i][j].delay + matrix[i][j].servicio
                            matrix[i][j + 1].arrival = matrix[i][j].leaving + 2

                            pasa = matrix[i][j].fila.dequeue()
                            matrix[i][j + 1].fila.enqueue(pasa)

                    else:
                        """Si el carro actual depende de algun carro enfrente entonces este compara el tiempo
                        de salida del carro que va enfrente de este para saber su delay y su arrival en la
                        estacion siguiente"""
                        if j == 16:
                            if matrix[i][j].arrival < matrix[subestacion1.ultimo1][lookhere].leaving:
                                matrix[i][j].delay = matrix[subestacion1.ultimo1][lookhere].leaving - matrix[i][j].arrival
                            else:
                                matrix[i][j].delay = 0
                            matrix[i][j].leaving = matrix[i][j].arrival + matrix[i][j].delay + matrix[i][j].servicio

                            matrix[i][18].arrival = matrix[i][j].leaving +2
                            subestacion.libre1 = True
                            subestacion.ultimo1 = i
                            pasa = matrix[i][j].fila.dequeue()
                            matrix[i][18].fila.enqueue(pasa)
                            lookhere = j

                        elif j == 17:
                            lookhere = j
                            if matrix[i][j].arrival < matrix[subestacion1.ultimo2][lookhere].leaving:
                                matrix[i][j].delay = matrix[subestacion1.ultimo2][lookhere].leaving - matrix[i][j].arrival
                            else:
                                matrix[i][j].delay = 0
                            matrix[i][j].leaving = matrix[i][j].arrival + matrix[i][j].delay + matrix[i][j].servicio

                            matrix[i][18].arrival = matrix[i][j].leaving +2
                            subestacion.libre2 = True
                            subestacion.ultimo2 = i
                            pasa = matrix[i][j].fila.dequeue()
                            matrix[i][18].fila.enqueue(pasa)
                            lookhere = j
                        elif j == 18:
                            if matrix[i][j].arrival < matrix[i-1][lookhere].leaving:
                                matrix[i][j].delay = matrix[i-1][lookhere].leaving - matrix[i][j].arrival
                            else:
                                matrix[i][j].delay = 0
                            matrix[i][j].leaving = matrix[i][j].arrival + matrix[i][j].delay + matrix[i][j].servicio

                            matrix[i][j + 1].arrival = matrix[i][j].leaving + 2
                            pasa = matrix[i][j].fila.dequeue()
                            matrix[i][j + 1].fila.enqueue(pasa)

                        else:

                            if matrix[i][j].arrival < matrix[i-1][j].leaving:
                                matrix[i][j].delay = matrix[i-1][j].leaving - matrix[i][j].arrival
                            else:
                                matrix[i][j].delay = 0
                            matrix[i][j].leaving = matrix[i][j].arrival + matrix[i][j].delay + matrix[i][j].servicio

                            matrix[i][j + 1].arrival = matrix[i][j].leaving + 2
                            pasa = matrix[i][j].fila.dequeue()
                            matrix[i][j + 1].fila.enqueue(pasa)

                else:
                    """Ya para el final, si un carro se encuentra en la ultima estacion, este lo que hace es
                    calcular su salida, su delay y simplemente se desasigna el mismo y no se asigna a otro lado
                    aqui termina cada carro su trayecto"""
                    if matrix[i][j].arrival < matrix[i-1][j].leaving:
                        matrix[i][j].delay = matrix[i-1][j].leaving - matrix[i][j].arrival
                    else:
                        matrix[i][j].delay = 0
                    matrix[i][j].leaving = matrix[i][j].arrival + matrix[i][j].delay + matrix[i][j].servicio
                    matrix[i][j].fila.dequeue()



            break

        """Este es el condicional que se encarga de terminar la simulacion, solo se cumple cuando no quedan mas
        carros que ensamblar en la linea"""
        if mainfila.isEmpty() == True and done == True:
            break

    """Se crea la siguiente lista para calcular el tiempo de espera de cada carro"""
    carrosdelay = [0 for i in range(ncarros)]
    for i in range(ncarros):
        tiempo += matrix[i][nestaciones-1].leaving - matrix[i][1].leaving
        for j in range(nestaciones):
            carrosdelay[i] += matrix[i][j].delay

    """Se imprimen los tiempos de cada carro en la simulacion"""
    for i in range(ncarros):
        for j in range(nestaciones):
            print(matrix[i][j].get())

    """Se imprime el tiempo de espera de cada carro"""
    for i in range(ncarros):
        print("El carro ",i+1," tuvo esperas de ", carrosdelay[i], " minutos en la linea")

    """Se imprime el tiempo total"""
    print("Tiempo total", tiempo)


if (__name__ == "__main__"):
    main()