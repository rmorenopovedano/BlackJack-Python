#!/usr/bin/env python
# -*- coding: utf-8 -*
'''
Created on 7/5/2015

@author: Raul Moreno Povedano
'''
from symbol import for_stmt

# EXTRAE UNA CARTA DE LA BARAJA
def extraerCarta(baraja):
    carta = random.choice(baraja)
    baraja.remove(carta)
    return carta

# REPARTE LA MANO PRINCIPAL (2 CARTAS A CADA JUGADOR)
def repartirCartasInicial():
    mano = []
    mano.append(extraerCarta(baraja))
    mano.append(extraerCarta(baraja))
    return mano

# CALCULA LA PUNTUACIÓN DE LAS CARTAS,
def calcularPuntuacionMano(manoActual):
    puntuacion = 0
    puntuacionTemp = 0
    tengoAs = 0
    tengoFigura = False
    blackjack = False
    # LEE LA PUNTUACIÓN MIENTRAS HAYA CARTAS EN LA MANO ACTUAL
    while len(manoActual) > 0 :
        # POP(): SACA UNA CARTA DE LA MANO ACTUAL
        muestra = manoActual.pop()
        # SEPARA EL VALOR DE LA CARTA 
        partes = muestra.split('_')
        valor = partes[0]
        # ASIGNAR VALORES A LAS CARTAS (J=10, Q=10, K=10)
        if valor == "J" or valor == "Q" or valor == "K" :
            puntuacion += 10
            tengoFigura = True
        elif valor == "A" :
            # LLEVAR UN CONTROL DE LOS ASES
            tengoAs += 1
        else :
            # AÑADE EL VALOR DE LA CARTA
            puntuacion += int(valor)
    # CAMBIAR EL VALOR DEL AS DEPENDIENDO DE LA PUNTUACION
    # SI TU PUNTACION ES MAYOR DE 10, EL AS VALE UN PUNTO
    # SI LA PUNTUACION ES 10 O MENOR, EL AS VALDRÁ 11 PUNTOS
    if puntuacion > 10 :
        puntuacion += tengoAs
    else :
        puntuacion += tengoAs * 10 + tengoAs
      
    return puntuacion
    

def jugarMesa(baraja, puntuacionJugador):
    manoActual = list(manoMesa)  # HACE UNA COPIA DE LA LISTA ACTUAL
    puntuacionMesa = calcularPuntuacionMano(manoActual)
    if puntuacionMesa > puntuacionJugador and puntuacionMesa < 22:  # LA BANCA TIENE OBLIGACIÓN DE SI TIENE MENOS DE 16 PUNTOS, 
                                                                    # PEDIR CARTA, PERO SI LA BANCA AL VALORAR SU PRIMERA MANO 
                                                                    # TIENE MEJOR PUNTUACIÓN QUE EL JUGADOR YA HA GANADO.
                                                                    
        return puntuacionMesa
    else:  # EN CASO DE QUE NO, SIGUE PIDIENDO CARTA HASTA QUE SE PASA DE 21
        while puntuacionMesa < 17:
            manoActual = list(manoMesa)
            puntuacionMesa = calcularPuntuacionMano(manoActual)
            if puntuacionMesa > puntuacionJugador and puntuacionMesa < 22:
                return puntuacionMesa
            elif puntuacionMesa < 17:
                manoMesa.append(extraerCarta(baraja))  # EXTRAE UNA CARTA DE LA BARAJA
        return puntuacionMesa

# PEDIR OPCION AL JUGADOR: PLANTARSE O PEDIR CARTA
def pedirOpcion(puntuacionJugador, manoActual):
    opcion = 0
    # HACER UNA COPIA DE LA MANO ACTUAL EN ESTE MOMENTO
    manoTemp = list(manoActual)
    while opcion != 1 and puntuacionJugador < 21:
        print "Tienes", puntuacionJugador, "puntos. ¿Qué quieres hacer?\n1. Plantarse\n2. Pedir carta"
        opcion = int(raw_input())
        # PLANTARSE
        if opcion == 1:
            plantarse(puntuacionJugador)
        # PEDIR CARTA
        elif opcion == 2 :
            manoTemp = list(pedirCarta(manoActual))
            puntuacionJugador = calcularPuntuacionMano(manoTemp)
        # CONTROLA QUE NO METAS UNA OPCION DISTINTA A 1 O 2
        else:
            print "Opción Incorrecta"
    return puntuacionJugador

# PIDE CARTA Y LA EXTRA DE LA BARAJA PARA AÑADIRLA A TU MANO ACTUAL
def pedirCarta(manoActual):
    manoActual.append(extraerCarta(baraja))
    print "Mano jugador: ", manoActual
    return manoActual

# COMPRUEBA SI TIENES BLACKJACK EN LA PRIMERA MANO
def comprobarBlackJack():
    tengoAs = False
    tengoFigura = False
    # EVALÚA LA PRIMERA CARTA  
    partes = manoActual[0].split('_')
    valor = partes[0]
    if valor == 'A':
        tengoAs = True
    elif valor == 'J' or valor == 'Q' or valor == 'K':
        tengoFigura = True
    else:
        return False
    # EVALÚA LA SEGUNDA CARTA
    partes = manoActual[1].split('_')
    valor = partes[0]
    if valor == 'A' and tengoFigura:
        return True
    elif (valor == 'J' or valor == 'Q' or valor == 'K') and tengoAs:
        return True
    else:
        return False

# TE PLANTAS Y MUESTRA TU PUNTUACIÓN FINAL   
def plantarse(puntuacionJugador):
    puntuacionJugadorFinal = puntuacionJugador
    print "Te has plantado con ", puntuacionJugadorFinal, "puntos"

# REALIZA LA COMPROBACIÓN DE QUIÉN HA GANADO
def comprobarGanador(puntuacionJugador, puntuacionMesa):
    global partidasGanadaJugador
    global partidasGanadaMesa
    # COMPRUBA QUE LA MESA SE HA PASADO
    if puntuacionMesa > 21:
        print "Tienes", puntuacionJugador, "puntos. !ENHORABUENA, HAS GANADO!"
        partidasGanadaJugador += 1
    # COMPRUEBA QUE LA PUNTUACIÓN DEL JUGADOR ES PEOR QUE LA DE LA MESA
    elif puntuacionJugador == puntuacionMesa:
        print "HA HABIDO UN EMPATE"
    elif puntuacionJugador<puntuacionMesa:
        print "LO SENTIMOS. LA BANCA GANA"
        partidasGanadaMesa+=1
    else:
        print "Tienes", puntuacionJugador, "puntos. !ENHORABUENA, HAS GANADO!"
        partidasGanadaJugador += 1
    
# MAIN
respuesta = 'S'
partidasGanadaMesa = 0
partidasGanadaJugador = 0
while respuesta.upper() == 'S': 
    if (__name__ == "__main__"):
        import string
        import random
        jugador = ""
        baraja = ['A_C', '2_C', '3_C', '4_C', '5_C', '6_C', '7_C', '8_C', '9_C', '10_C', 'J_C', 'Q_C', 'K_C',
                  'A_D', '2_D', '3_D', '4_D', '5_D', '6_D', '7_D', '8_D', '9_D', '10_D', 'J_D', 'Q_D', 'K_D',
                  'A_T', '2_T', '3_T', '4_T', '5_T', '6_T', '7_T', '8_T', '9_T', '10_T', 'J_T', 'Q_T', 'K_T',
                  'A_P', '2_P', '3_P', '4_P', '5_P', '6_P', '7_P', '8_P', '9_P', '10_P', 'J_P', 'Q_P', 'K_P']
        
        
        puntuacionJugador = 0
        # SALUDO INICIAL
        print "*******BIENVENIDO AL JUEGO DEL BLACKJACK********"
        jugador = raw_input("Introduce tu nombre: ")
        print "Hola", jugador        
        # JUGADOR COMIENZA A JUGAR
        manoJugador = repartirCartasInicial()
        print "Mano jugador: ", manoJugador
        # MESA COMIENZA A JUGAR
        manoMesa = repartirCartasInicial()
        print "Mano mesa: ", manoMesa[0]
        # CALCULA PUNTUACIONES DE LA PRIMERA MANO
        manoActual = list(manoJugador)
        if comprobarBlackJack():
            print "¡ENHORABUENA, TIENES BLACK JACK. HAS GANADOOOOO!"
            partidasGanadaJugador+=1
        else:
            puntuacionJugador = calcularPuntuacionMano(manoActual)
            manoActual = list(manoMesa)
            puntuacionMesa = calcularPuntuacionMano(manoActual)
            # PEDIR OPCIÓN AL JUGADOR SOBRE LO QUE QUIERE HACER
            manoActual = list(manoJugador)
            puntuacionJugador = pedirOpcion(puntuacionJugador, manoActual)
            if puntuacionJugador > 21:
                print puntuacionJugador, "PUNTOS. LO SIENTO TE HAS PASADO, LA BANCA GANA"
                partidasGanadaMesa+=1
            else:
                # JUEGA LA MESA
                manoActual = list(manoMesa)
                if comprobarBlackJack():
                    print "¡OHH,LA MESA TIENE BLACK JACK. LA BANCA GANA!"
                    partidasGanadaMesa+=1
                else:
                    puntuacionMesa = jugarMesa(baraja, puntuacionJugador)
                    print "Mano mesa: ", manoMesa
                    print "Puntuacion final mesa: ", puntuacionMesa
                    # COMPRUEBA QUIÉN HA GANADO LA PARTIDA
                    comprobarGanador(puntuacionJugador, puntuacionMesa)
    respuesta = ""
    while respuesta.upper() != 'S' and respuesta.upper() != 'N':         
        print "Desea volver a jugar?: (s/n)"
        respuesta = raw_input()
        if respuesta.upper() != 'S':
            print "El resultado final es:\nJugador:", partidasGanadaJugador, "\nMesa: ", partidasGanadaMesa
           
print "GRACIAS POR JUGAR A BLACK JACK. HASTA LA PRÓXIMA!!!"
                    

        
        
    
        
