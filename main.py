
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
#import sys



def main():
    #tworzenie aplikacji i okna
    app = QApplication([])
    window = QMainWindow()
    window.setGeometry(100, 100, 500, 350)
    window.setWindowTitle("Zadanie 6")
    #napis wybierz sygnal
    napis = QLabel(window)
    napis.setText("Wybierz sygnal Wejsciowy:")
    napis.setFont(QFont("Arial", 20))
    napis.resize(400, 50)
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
    app.exec_()





if __name__ == '__main__':
    main()

