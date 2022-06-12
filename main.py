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
    return n * silnia(n - 1) if n > 1 else 1


def potega(a, b):
    return a * potega(a, b - 1) if b > 0 else 1


def sinus(x):
    x %= 2 * PI
    x -= PI
    return -(x - potega(x, 3) / silnia(3) + potega(x, 5) / silnia(5) -
             potega(x, 7) / silnia(7) + potega(x, 9) / silnia(9))

def mcosinus(x): #ponieważ w obrazku do polecenia jako sinus ze składową stałą umieszczony jest tak naprawdę minus cosinus,
    x %= 2 * PI  #i jest on również bardziej realistycznym pobudzeniem, został on tutaj również zaimplementowany
    x -= PI      #należy go odkomentować w 213 linijce i zakomentować 212
    return (1 - potega(x, 2) / silnia(2) + potega(x, 4) / silnia(4) -
             potega(x, 6) / silnia(6) + potega(x, 8) / silnia(8))

def MatxVec(mac, wekt):
    w = [0] * 4
    for i in range(4):
        for j in range(4):
            w[i] += mac[i][j] * wekt[j]
    return w


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


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle("Dwie Ruchome Masy - Poćwiardowski, Rychter")
        self.setGeometry(100, 100, 1280, 720)
        self.figure = plt.figure()
        plt.subplots_adjust(left=0.1,
                            bottom=0.1,
                            right=0.95,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.35)

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.napis = QLabel(self)
        self.napis.setText("Wybierz sygnal wejściowy i jego parametry:")
        self.napis.setFont(QFont("Arial", 17))
        # radiobutton od fali prostokatniej
        self.prost = QRadioButton(self)
        self.prost.setText("Fala prostokątna")
        self.prost.setChecked(True)
        self.prost.setFont(QFont("Arial", 16))
        # radiobutton od skoku
        self.skok = QRadioButton(self)
        self.skok.setText("Skok")
        self.skok.setFont(QFont("Arial", 16))
        self.skok.move(5, 100)
        self.skok.resize(300, 40)
        # radiobutton od sinusoidy
        self.sinusoida = QRadioButton(self)
        self.sinusoida.setText("Sinusoida")
        self.sinusoida.setFont(QFont("Arial", 16))

        # importowanie i dodanie zdjecia
        czcionkaWpis = QFont("Arial", 14)
        self.mnz = QLabel(self)
        zdjecie = QPixmap("zadanie_6.png")
        zdjecie = zdjecie.scaledToHeight((400))
        self.mnz.setPixmap(zdjecie)
        self.mprost = QLabel(self)
        zdjecieProst = QPixmap("prost.jpg")
        self.mprost.setPixmap(zdjecieProst)
        self.mskok = QLabel(self)
        zdjecieSkok = QPixmap("skok.jpg")
        self.mskok.setPixmap(zdjecieSkok)
        self.msin = QLabel(self)
        zdjecieSin = QPixmap("sin.jpg")
        self.msin.setPixmap(zdjecieSin)
        # wartosci n do wpisania
        self.n_m1 = QLabel(self)
        self.n_m1.setText("Wartość m1: ")
        self.n_m1.setFont(QFont(czcionkaWpis))
        self.p_m1 = QLineEdit(self)
        self.p_m1.setText("1")
        self.p_m1.setFont(QFont(czcionkaWpis))
        self.n_m2 = QLabel(self)
        self.n_m2.setText("Wartość m2: ")
        self.n_m2.setFont(QFont(czcionkaWpis))
        self.p_m2 = QLineEdit(self)
        self.p_m2.setText("1")
        self.p_m2.setFont(QFont(czcionkaWpis))
        # wartosci k do wpisania
        self.n_k1 = QLabel(self)
        self.n_k1.setText("Wartość k1: ")
        self.n_k1.setFont(QFont(czcionkaWpis))
        self.p_k1 = QLineEdit(self)
        self.p_k1.setText("1")
        self.p_k1.setFont(QFont(czcionkaWpis))
        self.n_k2 = QLabel(self)
        self.n_k2.setText("Wartość k2: ")
        self.n_k2.setFont(QFont(czcionkaWpis))
        self.p_k2 = QLineEdit(self)
        self.p_k2.setText("1")
        self.p_k2.setFont(QFont(czcionkaWpis))
        # wartosci b do wpisania
        self.n_b1 = QLabel(self)
        self.n_b1.setText("Wartość b1: ")
        self.n_b1.setFont(QFont(czcionkaWpis))
        self.p_b1 = QLineEdit(self)
        self.p_b1.setText("1")
        self.p_b1.setFont(QFont(czcionkaWpis))
        self.n_b2 = QLabel(self)
        self.n_b2.setText("Wartość b2: ")
        self.n_b2.setFont(QFont(czcionkaWpis))
        self.p_b2 = QLineEdit(self)
        self.p_b2.setText("1")
        self.p_b2.setFont(QFont(czcionkaWpis))
        self.n_sila = QLabel(self)
        self.n_sila.setText("Wartość siły: ")
        self.n_sila.setFont(QFont(czcionkaWpis))
        self.p_sila = QLineEdit(self)
        self.p_sila.setText("2")
        self.p_sila.setFont(QFont(czcionkaWpis))
        # przycisk zapisania
        self.zapis = QPushButton(self)
        self.zapis.setText("Wykonaj symulację")
        self.zapis.setFont(QFont(czcionkaWpis))

        # po wcisnieciu przycisku wywolanie fukcji  zapis
        self.zapis.clicked.connect(
            lambda: self.Zapis(float(self.p_m1.text()), float(self.p_m2.text()), float(self.p_k1.text()),
                          float(self.p_k2.text()), float(self.p_b1.text()), float(self.p_b2.text()),
                          float(self.p_sila.text()), self.prost, self.skok, self.sinusoida))

        layout = QGridLayout()
        layout.addWidget(self.napis, 0, 0, 1, 4)
        layout.addWidget(self.prost, 1, 0, 1, 2)
        layout.addWidget(self.mprost, 2, 0, 1, 2)
        layout.addWidget(self.skok, 3, 0, 1, 2)
        layout.addWidget(self.mskok, 4, 0, 1, 2)
        layout.addWidget(self.sinusoida, 5, 0, 1, 2)
        layout.addWidget(self.msin, 6, 0, 1, 2)
        layout.addWidget(self.mnz, 1, 2, 6, 2)
        layout.addWidget(self.n_m1, 7, 0, 1, 1)
        layout.addWidget(self.p_m1, 7, 1, 1, 1)
        layout.addWidget(self.n_m2, 7, 2, 1, 1)
        layout.addWidget(self.p_m2, 7, 3, 1, 1)
        layout.addWidget(self.n_k1, 8, 0, 1, 1)
        layout.addWidget(self.p_k1, 8, 1, 1, 1)
        layout.addWidget(self.n_k2, 8, 2, 1, 1)
        layout.addWidget(self.p_k2, 8, 3, 1, 1)
        layout.addWidget(self.n_b1, 9, 0, 1, 1)
        layout.addWidget(self.p_b1, 9, 1, 1, 1)
        layout.addWidget(self.n_b2, 9, 2, 1, 1)
        layout.addWidget(self.p_b2, 9, 3, 1, 1)
        layout.addWidget(self.n_sila, 10, 0, 1, 1)
        layout.addWidget(self.p_sila, 10, 1, 1, 1)
        layout.addWidget(self.zapis, 10, 2, 1, 2)
        layout.addWidget(self.toolbar, 0, 4)
        layout.addWidget(self.canvas, 1, 4, 10, 1)
        self.setLayout(layout)

    def wykonanie(self, m1, m2, k1, k2, b1, b2, przebieg, F):
        A = [[0, 0, 1, 0],  #macierze
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
                u[i] = F if i > 0 else 0
            elif przebieg == 3:  # sinus
                u[i] = F / 2 * sinus(w * i * h) + F / 2
                #u[i] = F / 2 * mcosinus(w * i * h) + F / 2

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
            y1[i] = xi1[0]  # ponieważ D=0, a C1= [1 0 0 0], zależność C1x+Du upraszcza się do pierwszego elementu wektora xi
            y2[i] = xi1[1]  # ponieważ D=0, a C1= [0 1 0 0], zależność C1x+Du upraszcza się do drugiego elementu wektora xi

        self.figure.clear()
        ax1 = self.figure.add_subplot(211)
        ax1.plot(time, u)
        ax1.set_xlabel('czas t [s]')
        ax1.set_ylabel('siła F [N]')
        ax1.set_title('Wejście')
        ax1.legend(['u(t)'])
        ax1.grid(True)
        ax2 = self.figure.add_subplot(212)
        ax2.plot(time, y1)
        ax2.plot(time, y2)
        ax2.set_xlabel('czas t')
        ax2.set_ylabel('wychylenie x')
        ax2.legend(['x1(t)', 'x2(t)'])
        ax2.set_title('Wyjście')
        ax2.grid(True)
        self.canvas.draw()

    def Zapis(self, wpis_m1, wpis_m2, wpis_k1, wpis_k2, wpis_b1, wpis_b2, wpis_sila, prost, skok,
              sinusoida):  # przypisywanie wartosci do zmiennych
        m1 = wpis_m1
        m2 = wpis_m2
        k1 = wpis_k1
        k2 = wpis_k2
        b1 = wpis_b1
        b2 = wpis_b2
        sila = wpis_sila
        if prost.isChecked():
            przebieg = 1
        if skok.isChecked():
            przebieg = 2
        if sinusoida.isChecked():
            przebieg = 3
        if(m1>0 and m2 > 0 and k1 > 0 and k2 > 0 and b1>0 and b2 > 0): #sprawdzanie czy parametry są dodatnie
            self.wykonanie(m1, m2, k1, k2, b1, b2, przebieg, sila)
        else:
            QMessageBox.about(self, "Błąd", "Parametry układu muszą być większe od 0!")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()
    sys.exit(app.exec_())
