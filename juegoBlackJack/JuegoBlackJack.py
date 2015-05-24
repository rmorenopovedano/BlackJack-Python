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
        elif valor == "AS" :
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
    if valor == 'AS':
        tengoAs = True
    elif valor == 'J' or valor == 'Q' or valor == 'K':
        tengoFigura = True
    else:
        return False
    # EVALÚA LA SEGUNDA CARTA
    partes = manoActual[1].split('_')
    valor = partes[0]
    if valor == 'AS' and tengoFigura:
        return True
    elif (valor == 'J' or valor == 'Q' or valor == 'K') and tengoAs:
        return True
    else:
        return False

# TE PLANTAS Y MUESTRA TU PUNTUACIÓN FINAL   
def plantarse(puntuacionJugador):
    puntuacionJugadorFinal = puntuacionJugador
    print "Te has plantado con ", puntuacionJugadorFinal, "puntos\n"

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
# SALUDO INICIAL
print "*******BIENVENIDO AL JUEGO DEL BLACKJACK********"
jugador = raw_input("Introduce tu nombre: ")
print "Hola", jugador
while respuesta.upper() == 'S': 
    if (__name__ == "__main__"):
        import string
        import random
        jugador = ""
   

        baraja = ['AS_CORAZONES', '2_CORAZONES', '3_CORAZONES', '4_CORAZONES', '5_CORAZONES', '6_CORAZONES', '7_CORAZONES', '8_CORAZONES', '9_CORAZONES', '10_CORAZONES', 'J_CORAZONES', 'Q_CORAZONES', 'K_CORAZONES',
                  'AS_DIAMANTES', '2_DIAMANTES', '3_DIAMANTES', '4_DIAMANTES', '5_DIAMANTES', '6_DIAMANTES', '7_DIAMANTES', '8_DIAMANTES', '9_DIAMANTES', '10_DIAMANTES', 'J_DIAMANTES', 'Q_DIAMANTES', 'K_DIAMANTES',
                  'AS_TREBOLES', '2_TREBOLES', '3_TREBOLES', '4_TREBOLES', '5_TREBOLES', '6_TREBOLES', '7_TREBOLES', '8_TREBOLES', '9_TREBOLES', '10_TREBOLES', 'J_TREBOLES', 'Q_TREBOLES', 'K_TREBOLES',
                  'AS_PICAS', '2_PICAS', '3_PICAS', '4_PICAS', '5_PICAS', '6_PICAS', '7_PICAS', '8_PICAS', '9_PICAS', '10_PICAS', 'J_PICAS', 'Q_PICAS', 'K_PICAS']
        
        
        puntuacionJugador = 0
              
        # JUGADOR COMIENZA A JUGAR
        print "\t....MANO INICIAL....\n"
        manoJugador = repartirCartasInicial()
        print "Mano jugador: ", manoJugador
        # MESA COMIENZA A JUGAR
        manoMesa = repartirCartasInicial()
        print "Mano mesa: ", manoMesa[0],"\n"
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
            print "\t<<<<TURNO JUGADOR:>>>>"
            puntuacionJugador = pedirOpcion(puntuacionJugador, manoActual)
            if puntuacionJugador > 21:
                print puntuacionJugador, "PUNTOS. LO SIENTO TE HAS PASADO, LA BANCA GANA"
                partidasGanadaMesa+=1
            else:
                # JUEGA LA MESA
                manoActual = list(manoMesa)
                print "\t<<<<TURNO MESA:>>>>"
                if comprobarBlackJack():
                    print "¡OHH,LA MESA TIENE BLACK JACK. LA BANCA GANA!"
                    partidasGanadaMesa+=1
                else:
                    puntuacionMesa = jugarMesa(baraja, puntuacionJugador)
                    print "Mano mesa: ", manoMesa
                    print "Puntuacion final mesa: ", puntuacionMesa,"\n"
                    # COMPRUEBA QUIÉN HA GANADO LA PARTIDA
                    comprobarGanador(puntuacionJugador, puntuacionMesa)
    respuesta = ""
    while respuesta.upper() != 'S' and respuesta.upper() != 'N':         
        print "Desea volver a jugar?: (s/n)"
        respuesta = raw_input()
        if respuesta.upper() != 'S':
            print "El resultado final es:\nJugador:", partidasGanadaJugador, "\nMesa: ", partidasGanadaMesa
        else:
            print "El marcador va:\nJugador:", partidasGanadaJugador, "\nMesa: ", partidasGanadaMesa
           
print "GRACIAS POR JUGAR A BLACK JACK. HASTA LA PRÓXIMA!!!"
                    

        
        
    
        
