from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import sys

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

    xi1 = [0, 0, 0, 0]  # stan - warunki początkowe
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
    plt.legend(['x1(t)', 'x2(t)'])
    plt.grid(True)
    plt.show()

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setGeometry(100, 100, 1280, 720)
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        #self.canvas.setMaximumSize(480, 320)


        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        self.napis = QLabel(self)
        self.napis.setText("Wybierz sygnal Wejsciowy:")
        self.napis.setFont(QFont("Arial", 20))
        self.napis.resize(500, 50)
        self.napis.move(5, 0)
        # radiobutton od fali prostokatniej
        self.prost = QRadioButton(self)
        self.prost.setText("Fala prostokatna")
        self.prost.setChecked(True)
        self.prost.setFont(QFont("Arial", 16))
        self.prost.resize(300, 40)
        self.prost.move(5, 50)
        # radiobutton od skoku
        self.skok = QRadioButton(self)
        self.skok.setText("Skok")
        self.skok.setFont(QFont("Arial", 16))
        self.skok.move(5, 100)
        self.skok.resize(300, 40)
        # radiobutton od sinusoidy
        self.sinusoida = QRadioButton(self)
        self.sinusoida.setText("Sinusoida")
        self.sinusoida.move(5, 150)
        self.sinusoida.resize(300, 40)
        self.sinusoida.setFont(QFont("Arial", 16))

        # importowanie i dodanie zdjecia
        mnz = QLabel(self)
        zdjecie = QPixmap("zadanie_6.png")
        mnz.setPixmap(zdjecie)
        mnz.resize(202, 266)
        mnz.move(270, 50)
        # wartosci n do wpisania
        n_m1 = QLabel(self)
        n_m1.setText("Wartosc m1")
        n_m1.move(5, 225)
        p_m1 = QLineEdit(self)
        p_m1.setText("1")
        p_m1.move(5, 250)
        n_m2 = QLabel(self)
        n_m2.setText("Wartosc m2")
        n_m2.move(5, 275)
        p_m2 = QLineEdit(self)
        p_m2.setText("1")
        p_m2.move(5, 300)
        # wartosci k do wpisania
        n_k1 = QLabel(self)
        n_k1.setText("Wartosc k1")
        n_k1.move(620, 25)
        p_k1 = QLineEdit(self)
        p_k1.setText("1")
        p_k1.move(620, 50)
        n_k2 = QLabel(self)
        n_k2.setText("Wartosc k2")
        n_k2.move(620, 75)
        p_k2 = QLineEdit(self)
        p_k2.setText("1")
        p_k2.move(620, 100)
        # wartosci b do wpisania
        n_b1 = QLabel(self)
        n_b1.setText("Wartosc b1")
        n_b1.move(740, 25)
        p_b1 = QLineEdit(self)
        p_b1.setText("1")
        p_b1.move(740, 50)
        n_b2 = QLabel(self)
        n_b2.setText("Wartosc b2")
        n_b2.move(740, 75)
        p_b2 = QLineEdit(self)
        p_b2.setText("1")
        p_b2.move(740, 100)
        n_sila = QLabel(self)
        n_sila.setText("Wartosc sily")
        n_sila.move(860, 25)
        p_sila = QLineEdit(self)
        p_sila.setText("2")
        p_sila.move(860, 50)
        # przycisk zapisania
        zapis = QPushButton(self)
        zapis.setText("Zapisz")
        zapis.move(860, 100)

        # po wcisnieciu przycisku wywolanie fukcji  zapis
        zapis.clicked.connect(
            lambda: Zapis(float(p_m1.toPlainText()), float(p_m2.toPlainText()), float(p_k1.toPlainText()),
                          float(p_k2.toPlainText()), float(p_b1.toPlainText()), float(p_b2.toPlainText()),
                          float(p_sila.toPlainText()), self.prost, self.skok, self.sinusoida))

        
        layout = QGridLayout()
        layout.addWidget(self.napis, 0, 0, 1, 4)
        layout.addWidget(self.prost, 1, 0, 1, 2)
        layout.addWidget(self.skok, 2, 0, 1, 2)
        layout.addWidget(self.sinusoida, 3, 0, 1, 2)
        layout.addWidget(mnz, 1, 2, 3, 2)
        layout.addWidget(n_m1, 4, 0, 1, 1)
        layout.addWidget(p_m1, 4, 1, 1, 1)
        layout.addWidget(n_m2, 4, 2, 1, 1)
        layout.addWidget(p_m2, 4, 3, 1, 1)
        layout.addWidget(n_k1, 5, 0, 1, 1)
        layout.addWidget(p_k1, 5, 1, 1, 1)
        layout.addWidget(n_k2, 5, 2, 1, 1)
        layout.addWidget(p_k2, 5, 3, 1, 1)
        layout.addWidget(n_b1, 6, 0, 1, 1)
        layout.addWidget(p_b1, 6, 1, 1, 1)
        layout.addWidget(n_b2, 6, 2, 1, 1)
        layout.addWidget(p_b2, 6, 3, 1, 1)
        layout.addWidget(n_sila, 7, 0, 1, 1)
        layout.addWidget(p_sila, 7, 1, 1, 1)
        layout.addWidget(zapis, 7, 2, 1, 2)
        layout.addWidget(self.toolbar, 0, 4)
        layout.addWidget(self.canvas, 1, 4, 5, 1)
        layout.addWidget(self.button, 6, 4)
        self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [i for i in range(10)]

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

def main():
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
    prost.setChecked(True)
    prost.setFont(QFont("Arial", 16))
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
    mnz = QLabel(self)
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
    n_sila = QLabel(window)
    n_sila.setText("Wartosc sily")
    n_sila.move(860, 25)
    p_sila = QTextEdit(window)
    p_sila.setText("2")
    p_sila.move(860, 50)
    #przycisk zapisania
    zapis = QPushButton(window)
    zapis.setText("Zapisz")
    zapis.move(860, 100)
    figure = plt.figure()
    canvas = FigureCanvas(figure)
    layout = QVBoxLayout()
    layout.addWidget(canvas)
    window.setLayout(layout)

    #po wcisnieciu przycisku wywolanie fukcji  zapis
    zapis.clicked.connect(lambda: Zapis(float(p_m1.toPlainText()), float(p_m2.toPlainText()), float(p_k1.toPlainText()), float(p_k2.toPlainText()), float(p_b1.toPlainText()), float(p_b2.toPlainText()), float(p_sila.toPlainText()), prost, skok, sinusoida))



    window.show()

    app.exec_()
def Zapis(wpis_m1, wpis_m2, wpis_k1, wpis_k2, wpis_b1, wpis_b2, wpis_sila, prost, skok, sinusoida): #przypisywanie wartosci do zmiennych
    m1 = wpis_m1
    m2 = wpis_m2
    k1 = wpis_k1
    k2 = wpis_k2
    b1 = wpis_b1
    b2 = wpis_b2
    sila = wpis_sila
    print("m1:")
    print(m1)
    print("m2:")
    print(m2)
    print("k1:")
    print(k1)
    print("k2:")
    print(k2)
    print("b1:")
    print(b1)
    print("b2:")
    print(b2)
    print("sila:")
    print(sila)
    if prost.isChecked() == True:
        przebieg = 1
    if skok.isChecked() == True:
        przebieg = 2
    if sinusoida.isChecked() == True:
        przebieg = 3
    print("przebieg:")
    print(przebieg)
    wykonanie(m1, m2, k1, k2, b1, b2, przebieg, sila)







if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()
    sys.exit(app.exec_())
