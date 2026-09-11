#este programa se transformo a un juego
#el profesor me dijo que si me puedo adelantar con cosas y que lo unico que se debe calificar es lo actual
import time
from concurrent.futures import ThreadPoolExecutor
"""
===========================definicion de variables globales======================================
"""
dinero = 20 
yaSeParo=False
dia=1
"""
======================================variables del reloj=======================================
"""

t = 0
h = int(t/100)
m = t-(h*100)

"""
==================================funciones relacionadas al reloj=======================================
"""
def reloj():
   """
   recibe las variables globales de t, h, m que representan tiempo total hora y minutos
   hace que cuando los minutos llegan a 60 se añada una hora y no deja que las horas
   llegen a 24, cada vez que se ejecuta se añade un minuto y se muestra la hora en formato
   HH:MM
   """
   global t, h, m
   while (h <= 23 and m < 61):
       t = h * 100 + m
       m=m+1  
       if (m == 60):
           m = 0
           h = h+1
       if (m<10 and h<10):
           return("son las " + "0" + str(h) + ":" + "0" + str(m)) 
       elif (m<10):
           return("son las " + str(h) + ":" + "0" + str(m))
       elif (h<10):
           return("son las " + "0" + str(h) + ":" + str(m))
       else:
           return("son las " + str(h) + ":" + str(m)) 
   if (h==24):
    h=0
    m=0
def keepClockOn():
    while (True):
        """
        esta funcione hace que se ejecute cada 5 segundos la funcion del reloj 
        añadiendo un minuto de tiempo del juego a la hora
        """
        reloj()
        time.sleep(5)
"""
=========================================funciones del juego===============================================
"""

def menu():
    print ("bienvenido a")
    print (" ____  __  _  _  _  _  __     __   ____   __  ____    ____  ____     ___  _  _   __   _  _  ____   __  ")
    print (r"/ ___)(  )( \/ )/ )( \(  )   / _\ (    \ /  \(  _ \  (    \(  __)   / __)/ )( \ / _\ ( \/ )(  _ \ / _\ ")
    print (r"\___ \ )( / \/ \) \/ (/ (_/\/    \ ) D ((  O ))   /   ) D ( ) _)   ( (__ ) __ (/    \/ \/ \ ) _ (/    \ ")
    print (r"(____/(__)\_)(_/\____/\____/\_/\_/(____/ \__/(__\_)  (____/(____)   \___)\_)(_/\_/\_/\_)(_/(____/\_/\_/")
    seleccion = int(input("Juego Nuevo(1)                       cargar juego(2)          " \
    "       ver instrucciones(3) "))
    if (seleccion == 1):
                print ("cargando juego...")
                time.sleep(1)
                despertar()
    while (seleccion != 1):       
        if (seleccion == 3):
            print("tienes que trabajar, el tiempo no para de correr entonces tienes que ir rapido" \
            ", no te mueras de hambre y maneja bien tu dinero, el juego se acaba cuando te mueres" \
            " como la vida real")
            seleccion = int(input("juego nuevo(1)            cargar juego(2) "))
        elif (seleccion == 2):
            seleccion= int(input("esta opcion aun no esta disponible selecciona otra opcion "))
        else:
            seleccion = int(input("esa opcion no existe selecciona otra opcion"))


def despertar():
    global t,h,m
    print("tu alarma suena..." \
    "vez el reloj y son las 7 de la mañana")
    time.sleep(1)
    despertar = int(input("despertar(1)                     posponer(2) "))
    if (despertar == 2):
        print("pospones tu alarma 5 minutos y te quedas dormido")
        time.sleep(2)
        print("tu alarma sono pero no la escuchaste ahora son las 07:30 ")
        t = 730
        h=7
        m=30
        time.sleep(1)
        apartamento()
    elif (despertar == 1):
        print ("despertaste a tiempo")
        t = 700
        h=7
        m=0
        time.sleep(1)
        apartamento()     


def apartamento():
    global yaSeParo
    if (yaSeParo==False):
        print("te paras de tu cama y  vez alrededor")
        yaSeParo=True
    else:
        print ("volviste al centro del apartamento")
    time.sleep(1)
    accion = int(input("ver dinero (1)             ver hora(2)" \
    "        ir al baño(3)           ir a cocina(4)          salir de apartamento(5) "))
    if (accion == 3):
        baño()
    elif(accion == 4):
        cocina()
    elif(accion == 5):
        calle()
    while(accion!=3 or accion!=4 or accion!=5):
        if (accion == 1):
            print(dinero)
            accion = int(input("ver dinero (1)             ver hora(2)" \
                "        ir al baño(3)           ir a cocina(4)          salir de apartamento(5) "))
        elif (accion == 2):
           print(reloj())
           accion = int(input("ver dinero (1)             ver hora(2)" \
               "        ir al baño(3)           ir a cocina(4)          salir de apartamento(5) "))


def baño():
    print("esta parte aun no existe")
def cocina():
    print("esta parte aun no existe")
def calle():
    print("esta parte aun no existe")

"""
====================================parte para ejecutar las funciones del juego y las del reloj==============================
"""
#esta parte viene de stack overflow
def run_io_tasks_in_parallel(tasks):
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()

#esta tambien
run_io_tasks_in_parallel([
    lambda: menu(),
    lambda: keepClockOn(),
])