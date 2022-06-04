
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
import math
#import sys

PI = 3.14159265
N = 4
h = 0.001
T = 10.0
L = 2.5 # liczba okresów sygnału sinus w przedziale T
M = 8.0

class Wektor(object):
    def __init__(self, a1, a2, a3, a4):
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
    def __add__(self, other):
        return Wektor(self.a1 + other.a1, self.a2 + other.a2, self.a3 + other.a3, self.a4 + other.a4)
    def __mul__(self, other):
        return Wektor(self.a1 * other.a1, self.a2 * other.a2, self.a3 * other.a3, self.a4 * other.a4)
    def __mul__ (self, s):
        return Wektor(self.a1 * s, self.a2 * s, self.a3 * s, self.a4 * s)

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

def wykonanie(m1,m2,k1,k2,b1,b2):
    A=[[0,0,1,0],
       [0,0,0,1],
       [(-k1-k2)/m1, k2/m1, (-b1-b2)/m1, b2/m1],
       [k2/m2, -k2/m2, b2/m2, -b2/m2]]
    B=[0,0,0,1/m2]
    C1=[1, 0, 0, 0]
    C2=[0, 1, 0, 0]
    D=0
    Ax = []
    Bu = []
    w = 2.0 * PI * L / T
    acc = int(T/h) + 1
    usin = [0] * acc
    usq = [0] * acc
    usk = M
    time = [0] * acc
    y1 = [0] * acc
    y2 = [0] * acc
    for i in range(acc):
        time[i] = i*h
        usin[i] = M * math.sin(w * i * h) + M
        usq[i] = M if usin[i]>0 else -M

    xi1 = [0] * 4

    for i in range(acc):
        Ax = MatxVec(A, xi1)
        Bu = VecxSkal(B, usin[i])
        C1x = VecxVec(C1, xi1)
        C2x = VecxVec(C2, xi1)
        Du = D*usin[i]
        xi = VecplusVec(Ax,Bu)
        xi = VecxSkal(xi, h)
        xi= VecplusVec(xi, xi1)
        xi1=xi
        y1[i]=C1x+Du
        y2[i]=C2x+Du

    plt.plot(time, y1)
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

    wykonanie(1,1,1,1,1,1)





    window.show()
    app.exec_()





if __name__ == '__main__':
    main()

