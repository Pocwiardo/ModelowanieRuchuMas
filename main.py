from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
# import sys

PI = 3.14159265
h = 0.001  # krok całkowania
T = 10.0  # czas symulacji
f = 1  # częstotliwość
L = 2.0

def silnia(n):
    return n*silnia(n-1) if n > 1 else 1

def potega(a, b):
    return a*potega(a, b-1) if b > 0 else 1

def sinus(x):
    x %= 2*PI
    x-=PI
    return -(x-potega(x,3)/silnia(3)+potega(x,5)/silnia(5)-potega(x,7)/silnia(7)+potega(x,9)/silnia(9))

def MatxVec(mac, wekt):
    w = [0] * 4
    for i in range(4):
        for j in range(4):
            w[i] += mac[i][j] * wekt[j]
    return w


def VecxVec(wekt1, wekt2):
    s = 0
    for i in range(4):
        s += wekt1[i] * wekt2[i]
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


def wykonanie(m1, m2, k1, k2, b1, b2, przebieg, F):
    A = [[0, 0, 1, 0],
         [0, 0, 0, 1],
         [(-k1 - k2) / m1, k2 / m1, (-b1 - b2) / m1, b2 / m1],
         [k2 / m2, -k2 / m2, b2 / m2, -b2 / m2]]
    B = [0, 0, 0, 1 / m2]

    w = 2.0 * PI * L / T
    acc = int(T / h) + 1  # ilość kroków całkowania, "rozdzielczość" wykresu w pewnym sensie
    time = [0] * acc
    u = [0] * acc
    y1 = [0] * acc
    y2 = [0] * acc
    for i in range(acc):
        time[i] = i * h
        if przebieg == 1:  # prostokat
            u[i] = F if sinus(w * i * h) > 0 else 0
        elif przebieg == 2:  # skok
            u[i] = F
        elif przebieg == 3:  # sinus
            u[i] = F / 2 * sinus(w * i * h) + F / 2
            #u[i] = F / 2 * math.sin(w * i * h) + F / 2

    xi1 = [0, 0, 0, 0]  # stan - warunki początkowe, trzeba się zastanowić czy nie oznaczają one czasem już naciągnięcia sprężyn Edit: oznaczają, musi być 0
    xip = [0] * 4  # poprzednia wartość x'

    for i in range(acc):
        Ax = MatxVec(A, xi1)
        Bu = VecxSkal(B, u[i])
        xi = VecplusVec(Ax, Bu)  # nowe x'
        xcalk = VecplusVec(xi, xip)
        xip = xi
        xcalk = VecxSkal(xcalk, h / 2)
        xcalk = VecplusVec(xcalk, xi1)  # zsumowanie fragmentu z poprzednią całką (całka w nowym punkcie)
        xi1 = xcalk
        y1[i] = xi1[
            0]  # ponieważ D=0, a C1= [1 0 0 0], zależność C1x+Du upraszcza się do pierwszego elementu wektora xi
        y2[i] = xi1[1]  # ponieważ D=0, a C1= [0 1 0 0], zależność C1x+Du upraszcza się do drugiego elementu wektora xi

    plt.plot(time, u)
    plt.plot(time, y1)
    plt.plot(time, y2)
    plt.xlabel('czas t')
    plt.ylabel('wychylenie x')
    plt.legend(['u(t)', 'x1(t)', 'x2(t)'])
    plt.show()


def main(m1=1, m2=1, k1=1, k2=1, b1=1, b2=1):
    # tworzenie aplikacji i okna
    app = QApplication([])
    window = QMainWindow()
    window.setGeometry(100, 100, 1280, 720)
    window.setWindowTitle("Zadanie 6")
    # napis wybierz sygnal
    napis = QLabel(window)
    napis.setText("Wybierz sygnal Wejsciowy:")
    napis.setFont(QFont("Arial", 20))
    napis.resize(500, 50)
    napis.move(5, 0)
    # radiobutton od fali prostokatniej
    prost = QRadioButton(window)
    prost.setText("Fala prostokatna")
    prost.setFont(QFont("Arial", 16))
    prost.setChecked(True)
    prost.resize(300, 40)
    prost.move(5, 50)
    # radiobutton od skoku
    skok = QRadioButton(window)
    skok.setText("Skok")
    skok.setFont(QFont("Arial", 16))
    skok.move(5, 100)
    skok.resize(300, 40)
    # radiobutton od sinusoidy
    sinusoida = QRadioButton(window)
    sinusoida.setText("Sinusoida")
    sinusoida.move(5, 150)
    sinusoida.resize(300, 40)
    sinusoida.setFont(QFont("Arial", 16))
    # importowanie i dodanie zdjecia
    mnz = QLabel(window)
    zdjecie = QPixmap("zadanie_6.png")
    mnz.setPixmap(zdjecie)
    mnz.resize(202, 266)
    mnz.move(270, 50)
    #wartosci n do wpisania
    n_m1 = QLabel(window)
    n_m1.setText("Wartosc m1")
    n_m1.move(500, 25)
    p_m1 = QTextEdit(window)
    p_m1.setText("1")
    p_m1.move(500, 50)
    n_m2 = QLabel(window)
    n_m2.setText("Wartosc m2")
    n_m2.move(500, 75)
    p_m2 = QTextEdit(window)
    p_m2.setText("1")
    p_m2.move(500, 100)
    #wartosci k do wpisania
    n_k1 = QLabel(window)
    n_k1.setText("Wartosc k1")
    n_k1.move(620, 25)
    p_k1 = QTextEdit(window)
    p_k1.setText("1")
    p_k1.move(620, 50)
    n_k2 = QLabel(window)
    n_k2.setText("Wartosc k2")
    n_k2.move(620, 75)
    p_k2 = QTextEdit(window)
    p_k2.setText("1")
    p_k2.move(620, 100)
    #wartosci b do wpisania
    n_b1 = QLabel(window)
    n_b1.setText("Wartosc b1")
    n_b1.move(740, 25)
    p_b1 = QTextEdit(window)
    p_b1.setText("1")
    p_b1.move(740, 50)
    n_b2 = QLabel(window)
    n_b2.setText("Wartosc b2")
    n_b2.move(740, 75)
    p_b2 = QTextEdit(window)
    p_b2.setText("1")
    p_b2.move(740, 100)
    #przycisk zapisania
    zapis = QPushButton(window)
    zapis.setText("Zapisz")
    zapis.move(860, 75)
    #po wcisnieciu przycisku wywolanie fukcji  zapis
    zapis.clicked.connect(lambda: Zapis(float(p_m1.toPlainText()), float(p_m2.toPlainText()), float(p_k1.toPlainText()), float(p_k2.toPlainText()), float(p_b1.toPlainText()), float(p_b2.toPlainText())))



    window.show()

    app.exec_()
def Zapis(wpis_m1, wpis_m2, wpis_k1, wpis_k2, wpis_b1, wpis_b2): #przypisywanie wartosci do zmiennych
    m1 = wpis_m1
    m2 = wpis_m2
    k1 = wpis_k1
    k2 = wpis_k2
    b1 = wpis_b1
    b2 = wpis_b2
    print("m1")
    print(m1)
    print("m2")
    print(m2)
    print("k1")
    print(k1)
    print("k2")
    print(k2)
    print("b1")
    print(b1)
    print("b2")
    print(b2)
    wykonanie(m1, m2, k1, k2, b1, b2, 3, 2.0)

if __name__ == '__main__':
    main()
