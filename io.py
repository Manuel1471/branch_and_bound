import random as rand
import math
from scipy.optimize import linprog
import copy
import os
import time


class Arbol(object):
    def __init__(self):
        self.der = None		# Rama derecha del árbol
        self.izq = None		# Rama izquierda del árbol
        self.resultado = None		# Resultado del nodo del árbol
        self.enteros = None
        self.con_solucion = None
        self.c = None
        self.A_ub = None
        self.b_ub = None
        self.A_eq = None
        self.b_eq = None

resultados = []

def rellenar(num_var, var, signo):
    lista = []
    for i in range(0, num_var):
        if (var == i and signo == "<="):
            lista.append(1)
        elif (var == i and signo == ">="):
            lista.append(-1)
        else:
            lista.append(0)
    return lista


def no_enteras(rama):
    return [rama.resultado.x[i] if not rama.resultado.x[i].is_integer() else 0 for i in range(len(rama.c))]


def insertar(rama, lado_derecho, variable, signo):
    restriccion = rellenar(len(rama.c), variable, signo)
    if signo == '<=':
        rama.izq = copy.deepcopy(rama)
        rama.izq.resultado = None
        rama.izq.A_ub.append(restriccion)
        rama.izq.b_ub.append(lado_derecho)
    if signo == '>=':
        rama.der = copy.deepcopy(rama)
        rama.der.resultado = None
        rama.der.A_ub.append(restriccion)
        rama.der.b_ub.append(lado_derecho*-1)
    return rama


def comparar(lista1, lista2):
    if len(lista2) == 0:
        return 1
    else:
        for i in range(0, len(lista1)):
            if(lista1[i] != lista2[i]):
                return None
        return 1


def branch(rama, tipofuncion):
    son_enteras = no_enteras(rama)
    ld_nuevo = 0
    variable = 0
    while(ld_nuevo == 0):
        variable = rand.randrange(0, len(son_enteras))
        ld_nuevo = son_enteras[variable]

    rama = insertar(rama, math.floor(ld_nuevo), variable, '<=')
    algoritmo_branch_and_bound(rama.izq, tipofuncion)
    rama = insertar(rama, math.ceil(ld_nuevo), variable, '>=')
    algoritmo_branch_and_bound(rama.der, tipofuncion)
    # os.system('clear')
    # os.system('cls')


def inicio(c, A_ub, b_ub, tipofuncion):
    raiz = Arbol()
    raiz.c = c
    raiz.A_ub = A_ub
    raiz.b_ub = b_ub
    algoritmo_branch_and_bound(raiz, tipofuncion)
    #os.system('clear')
    #os.system('cls')
    #os.system('clear')
    resultado_final = 0
    for resultado in resultados:
        if resultado_final == 0:
            resultado_final = resultado
        else:
            if tipofuncion == 'maximizar' and resultado_final.fun <= resultado.fun:
                resultado_final = resultado
            if tipofuncion == 'minimizar' and resultado_final.fun >= resultado.fun:
                resultado_final = resultado
    if resultado_final != 0:
        print("\nSolucion optima:", resultado_final.fun, "\n")
        print("Variables optimas:", resultado_final.x, "\n")
    else:
        print("\nEste problema no tiene solución")


def algoritmo_branch_and_bound(rama, tipofuncion):
    simplex(rama, tipofuncion)

    if (not rama.resultado.fun.is_integer() or True in [not x.is_integer() for x in rama.resultado.x]) and rama.con_solucion == True:
        branch(rama, tipofuncion)
        # os.system('clear')
        # os.system('cls')
    elif rama.con_solucion:
        rama.enteros = True
        resultados.append(rama.resultado)
        # os.system('clear')
        # os.system('cls')


def simplex(rama, tipofuncion):
                                    # c son los coeficientes de las variables de la funcion objetivo
                                    # A_ub son los coeficientes de las restricciones funcionales en una matriz siendo solo las <=
                                    # b_ub son los coeficientes del lado derecho de las restricciones de A_ub
    if tipofuncion == "maximizar":
        res = linprog(rama.c, rama.A_ub, rama.b_ub, bounds=(0, None), method="simplex")
        res.fun = res.fun*-1
        rama.resultado = res
        rama.con_solucion = rama.resultado.success
        return None
    else:
        rama.resultado = linprog(rama.c, rama.A_ub, rama.b_ub, bounds=(0, None), method="simplex")
        rama.con_solucion = rama.resultado.success
        return None


def menu():
    c = []
    A_ub = []
    b_ub = []
    lineas = []
    with open('problema.txt', 'r') as f:
        for linea in f:
            if linea.strip() != '':
                lineas.append(linea.split())
    f.close()
    respuesta = lineas[0][0]
    c_variables = len(lineas[0])
    for i in range(1, c_variables):
        c.append(int(lineas[0][i]))

    if respuesta == 'maximizar':
        c = convertir_vector(c)

    for i in range(1, len(lineas)):
        auxiliar = []
        for j in range(0, c_variables-1):
            auxiliar.append(int(lineas[i][j]))
        if(lineas[i][c_variables-1] == '>='):
            auxiliar = convertir_vector(auxiliar)
            b_ub.append(int(lineas[i][c_variables])*-1)
            A_ub.append(auxiliar)
        else:
            b_ub.append(int(lineas[i][c_variables]))
            A_ub.append(auxiliar)

    #print('tipo de problema',respuesta,'\n')
    #print('coeficientes del modelo',c,'\n')
    #print('coeficientes de restricciones',A_ub,'\n')
    #print('coeficientes del lado derecho',b_ub,'\n')
    inicio(c, A_ub, b_ub, respuesta)


def convertir_vector(s):
    lista = []
    for x in s:
        lista.append(x*-1)
    return lista


menu()
