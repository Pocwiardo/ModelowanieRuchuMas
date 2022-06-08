
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
import math
#import sys

PI = 3.14159265
h = 0.001 #krok całkowania
T = 10.0 #czas symulacji
f = 0.4 #częstotliwość


def MatxVec(mac, wekt):
    w = [0] * 4
    for i in range(4):
        for j in range(4):
            w[i]+= mac[i][j] * wekt[j]
    return w
def VecxVec(wekt1, wekt2):
    s=0
    for i in range(4):
        s+= wekt1[i] * wekt2[i]
    return s
def VecxSkal(wekt, skal):
    w = [0] * 4
    for i in range(4):
        w[i] = wekt[i] * skal
    return w
def VecplusVec(wekt1, wekt2):
    w = [0] * 4
    for i in range(4):
        w[i] = wekt1[i] + wekt2[i]
    return w



def wykonanie(m1,m2,k1,k2,b1,b2, przebieg, F):
    A=[[0,0,1,0],
       [0,0,0,1],
       [(-k1-k2)/m1, k2/m1, (-b1-b2)/m1, b2/m1],
       [k2/m2, -k2/m2, b2/m2, -b2/m2]]
    B=[0,0,0,1/m2]
    
    w = 2.0 * PI * f
    acc = int(T/h) + 1 #ilość kroków całkowania, "rozdzielczość" wykresu w pewnym sensie
    time = [0] * acc
    u = [0] * acc
    y1 = [0] * acc
    y2 = [0] * acc
    for i in range(acc):
        time[i] = i*h
        if przebieg == 1: #prostokat
            u[i] = F if math.sin(w * i * h) > 0 else 0
        elif przebieg == 2: #skok
            u[i] = F
        elif przebieg == 3: #sinus
            u[i] = F/2 * math.sin(w * i * h) + F/2


    xi1 = [1, 2, 0, 0] #stan - warunki początkowe, warto dodać ustawianie ich w oknie na konkretne wartości
    xip = [0] * 4 #poprzednia wartość x'


    for i in range(acc):
        Ax = MatxVec(A, xi1)
        Bu = VecxSkal(B, u[i])
        xi = VecplusVec(Ax, Bu) #nowe x'
        xcalk = VecplusVec(xi, xip)
        xip=xi
        xcalk = VecxSkal(xcalk, h/2)
        xcalk = VecplusVec(xcalk, xi1) #zsumowanie fragmentu z poprzednią całką (całka w nowym punkcie)
        xi1 = xcalk
        y1[i] = xi1[0] #ponieważ D=0, a C1= [1 0 0 0], zależność C1x+Du upraszcza się do pierwszego elementu wektora xi
        y2[i] = xi1[1] #ponieważ D=0, a C1= [0 1 0 0], zależność C1x+Du upraszcza się do drugiego elementu wektora xi

    plt.plot(time, u)
    plt.plot(time, y1)
    plt.plot(time, y2)
    plt.xlabel('czas t')
    plt.ylabel('wychylenie x')
    plt.legend(['u(t)','x1(t)','x2(t)'])
    plt.show()


def main():
    #tworzenie aplikacji i okna
    app = QApplication([])
    window = QMainWindow()
    window.setGeometry(100, 100, 1280, 720)
    window.setWindowTitle("Zadanie 6")
    #napis wybierz sygnal
    napis = QLabel(window)
    napis.setText("Wybierz sygnal Wejsciowy:")
    napis.setFont(QFont("Arial", 20))
    napis.resize(500, 50)
    napis.move(5,0)
    #radiobutton od fali prostokatniej
    prost = QRadioButton(window)
    prost.setText("Fala prostokatna")
    prost.setFont(QFont("Arial", 16))
    prost.setChecked(True)
    prost.resize(300, 40)
    prost.move(5, 50)
    #radiobutton od skoku
    skok = QRadioButton(window)
    skok.setText("Skok")
    skok.setFont(QFont("Arial", 16))
    skok.move(5, 100)
    skok.resize(300, 40)
    #radiobutton od sinusoidy
    sinusoida = QRadioButton(window)
    sinusoida.setText("Sinusoida")
    sinusoida.move(5, 150)
    sinusoida.resize(300, 40)
    sinusoida.setFont(QFont("Arial", 16))
    #importowanie i dodanie zdjecia
    mnz = QLabel(window)
    zdjecie = QPixmap("zadanie_6.png")
    mnz.setPixmap(zdjecie)
    mnz.resize(202, 266)
    mnz.move(270,50)

    window.show()
    wykonanie(1, 1, 1, 1, 1, 1, 1, 2.0)
    app.exec_()


if __name__ == '__main__':
    main()

