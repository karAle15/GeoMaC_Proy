# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 14:27:10 2020.

@author: luiggi

Modificado por: Karina A. Rodríguez Ramírez
Fecha: Oct 21. 2021

"""
import numpy as np
from scipy import interpolate

def calcDth(Dth_data, z, N):
    """
    Genera un arreglo de tamaño N+2 que contiene la información
    de la difusividad de acuerdo con la profundidad.

    Parameters
    ----------
    Dth_data : ARRAY
        VALORES DE LA COEFICIENTE DE DIFUSIVIDAD CALCULADA.
    z : ARREGLO
        COORDENADA Z DE LA PROFUNDIDAD.
    N : ENTERO
        TAMAÑO DE LA MATRIZ.

    Returns
    -------
    Dth : ARRAY
        Información de Dth de acuerdo con la profundidad.

    """
    Dth = np.zeros((N+2))
    for k in range(0, N+2):
        if (z[k] <= 50.0):
            Dth[k] = Dth_data[0]
        elif ((z[k] > 50.0) and (z[k] <= 250.0)):
            Dth[k] = Dth_data[1]
        elif ((z[k] > 250.0) and (z[k] <= 400.0)):
            Dth[k] = Dth_data[2]
        elif ((z[k] > 400.0) and (z[k] <= 600.0)):
            Dth[k] = Dth_data[3]
        elif ((z[k] > 600.0) and (z[k] <= 800.0)):
            Dth[k] = Dth_data[4]
        elif ((z[k] > 800.0) and (z[k] <= 1000.0)):
            Dth[k] = Dth_data[5]
        elif ((z[k] > 1000.0) and (z[k] <= 1500.0)):
            Dth[k] = Dth_data[6]
        elif ((z[k] > 1500.0) and (z[k] <= 1900.0)):
            Dth[k] = Dth_data[7]
        else:
            Dth[k] = Dth_data[8]
    return Dth

def interpTemp(z_dat, T_dat, z):
    """
    Realiza las interpolaciones de las temperaturas
    a las profundidades donde se hará el cálculo.

    Parameters
    ----------
    z_dat : ARREGLO
        Profundidades a interpolar.
    T_dat : ARREGLO
        Temperaturas a interpolar.
    z : ARREGLO
        Coordenada Z de la profundidad.

    Returns
    -------
    T_ini : ARREGLO
        Arreglo con las interpolaciones.

    """
    tck_1 = interpolate.splrep(z_dat, T_dat)
    T_ini = interpolate.splev(z, tck_1)
    return T_ini

def arithmeticMean(a, b):
    """
    Calcula la media aritmética entre a y b.
    
    Parameters
    ----------
    a, b: int
    Valores a interpolar.
    
    Returns
    -------
    La media aritmética.
    """
    return 0.5 * (a + b)

def harmonicMean(a, b):
    """
    Calcula la media armónica entre a y b.
    
    Parameters
    ----------
    a, b: int
    Valores a interpolar.
    
    Returns
    -------
    La media armónica.
    """    
    return 2 * a * b / (a + b)
    
def Laplaciano1D(N, d, f=None):
    """
    Calcula la matriz del Laplaciano usando diferencias finitas en 1D.
    
    Parameters
    ----------
    N: int
    Tamaño de la matriz
    
    d: float
    Valores del coeficiente Gamma de la ecuación.
    
    f: function
    Función para calcular el promedio entre dos valores.
    
    Returns
    -------
    A: ndarray
    La matriz del sistema.
    """
    if f == None:
        A = np.zeros((N,N))
        A[0, 0] = -2 * d[1]
        A[0, 1] = d[1]
        
        for i in range(1,N-1):
            A[i,i] = -2 * d[i+1]
            A[i,i+1] = d[i+1] #harmonicMean(d[i], d[i+1])
            A[i,i-1] = d[i] #harmonicMean(d[i], d[i+1])
            
        A[N-1,N-2] = d[N]
        A[N-1,N-1] = -2 * d[N]

    else:        
        A = np.zeros((N,N))
        A[0, 0] -= ( f(d[0], d[1]) + f(d[1], d[2]) )
        A[0, 1] = f(d[1], d[2])
        
        for i in range(1,N-1):
            A[i,i] -= ( f(d[i], d[i+1]) + f(d[i+1], d[i+2]) )
            A[i,i+1] = f(d[i+1], d[i+2])
            A[i,i-1] = f(d[i+1], d[i])

        A[N-1,N-2] = f(d[N-1], d[N])
        A[N-1,N-1] -= ( f(d[N-1], d[N]) + f(d[N], d[N+1]) )

    return A


def Laplaciano1D_NS(N, d, f=None):
    """
    Calcula la matriz del Laplaciano usando diferencias finitas en 1D.
    
    Parameters
    ----------
    N: int
    Tamaño de la matriz
    
    d: float
    Valores del coeficiente Gamma de la ecuación.
    
    f: function
    Función para calcular el promedio entre dos valores.
    
    Returns
    -------
    A: ndarray
    La matriz del sistema.
    """
    if f == None:
        A = np.zeros((N,N))
        A[0, 0] = ( 2 * d[1] + 1 )
        A[0, 1] = -d[1]

        for i in range(1,N-1):
            A[i,i] = ( 2 * d[i+1] + 1 )
            A[i,i+1] = -harmonicMean(d[i], d[i+1])
            A[i,i-1] = -harmonicMean(d[i], d[i+1])

        A[N-1,N-2] = -d[N]
        A[N-1,N-1] = ( 2 * d[N] + 1)

    else:     
        A = np.zeros((N,N))
        A[0, 0] = ( f(d[0], d[1]) + f(d[1], d[2]) + 1 )
        A[0, 1] = -f(d[1], d[2])    
        for i in range(1,N-1):
            A[i,i] = ( f(d[i], d[i+1]) + f(d[i+1], d[i+2]) + 1 )
            A[i,i+1] = -f(d[i+1], d[i+2])
            A[i,i-1] = -f(d[i+1], d[i])

        A[N-1,N-2] = -f(d[N-1], d[N])
        A[N-1,N-1] = ( f(d[N-1], d[N]) + f(d[N], d[N+1]) + 1)


    
    return A
#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':
    
    print('Arithmetic (1, 2) : {}'.format(arithmeticMean(1,2)))
    print('Harmonic (1,2) : {} \n'.format(harmonicMean(1,2)))
    input('Press enter')

    N = 5
    gamma = np.random.rand(N+2)
    print('Gamma:{}'.format(gamma))

    # Interpolación de la Gamma en los puntos medios
    gammaAM = [arithmeticMean(gamma[i], gamma[i+1]) for i in range(0, len(gamma)-1)]
    gammaHM = [harmonicMean(gamma[i], gamma[i+1]) for i in range(0, len(gamma)-1)]

    print('Gamma (Arithmetic):{}'.format(gammaAM))
    print('Gamma (Harmonic):{} \n'.format(gammaHM))

    input('Press enter')

    # Graficación de las Gammas
    import matplotlib.pyplot as plt
    h = 1.0 / (N+1)
    x = np.linspace(0,1,N+2)
    xm = x[:-1] + h * 0.5
    plt.plot(x, gamma, 'o-', label='Original', lw=2)
    plt.plot(xm, gammaAM, 's--', label='Prom. Aritmético', lw=1.0)
    plt.plot(xm, gammaHM, 'v--', label='Media Armónica', lw=1.0)
    plt.xlabel('x')
    plt.ylabel('Gamma')
    plt.xticks(x)
    plt.grid(ls='--')
    plt.legend()
    plt.show()
    
    input('Press enter')
    
    # Creación de las matrices
    print('None:\n{}'.format(Laplaciano1D(N, gamma)))
    print('Arithmetic:\n{}'.format(Laplaciano1D(N, gamma, arithmeticMean)))
    print('Harmonic:\n{}'.format(Laplaciano1D(N, gamma, harmonicMean)))
    print('NS Arithmetic:\n{}'.format(Laplaciano1D_NS(N, gamma, arithmeticMean)))
    print('NS Harmonic:\n{}'.format(Laplaciano1D_NS(N, gamma, harmonicMean)))
    
