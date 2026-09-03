pagoPosicion1 = 100
pagoPosicion2 = 50
pagoPosicion3 = 125
posicion = 0
diaOSemana = 0
pago = 0
print("ingresa tu posicion ")
while (posicion != 1 and posicion != 2 and posicion != 3):
    posicion = int(input("para posicion 1 ingrese 1" \
    " para posicion 2 ingrese 2 para posicion 3 ingrese 3 "))
if (posicion == 1):
    posicion = pagoPosicion1
elif (posicion == 2):
    posicion = pagoPosicion2
else:
    posicion = pagoPosicion3
while (diaOSemana != 1 and diaOSemana != 2):
    diaOSemana = int(input("para calcular por dia ingrese 1" \
    " para calcular por semana ingrese 2 "))
horasTrabajadas = float(input("ingrese cuantas horas trabajo "))
if (diaOSemana == 1):
    if (horasTrabajadas <= 8):
        pago = posicion * horasTrabajadas
    else:
        horasTrabajadas = horasTrabajadas - 8
        pago = (posicion * horasTrabajadas * 1.5) + (8 * posicion)
else:
    if (horasTrabajadas <= 40):
        pago = posicion * horasTrabajadas
    else:
        horasTrabajadas = horasTrabajadas - 40
        pago = (posicion * horasTrabajadas * 1.5) + (40 * posicion)
print ("tu pago son " + str(pago) + " pesos")