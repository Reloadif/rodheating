import matplotlib
import matplotlib.pyplot as pyplot

matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from MainWindow import Ui_MainWindow
from Modules import *

import sys, os, os.path

class MainMatplotWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainMatplotWindow, self).__init__()

        self.userInterface = Ui_MainWindow()
        self.userInterface.setupUi(self)

        self.figure = pyplot.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.userInterface.verticalLayout.addWidget(self.toolbar)
        self.userInterface.verticalLayout.addWidget(self.canvas)

        icondir = ""
        if hasattr(sys, "_MEIPASS"): icondir = os.path.join(sys._MEIPASS, './icons/mainIcon.png')
        else: icondir = './icons/mainIcon.png'
        self.setWindowIcon(QtGui.QIcon(icondir))

        self.setHandlers()
        self.setValidators()

        self.dataContext = DataContext()
        self.resultSolution = None
    
    def setHandlers(self):
        self.userInterface.ClearSheduleButton.clicked.connect(self.onClickClearSheduleButton)
        self.userInterface.RunCalculateButton.clicked.connect(self.onClickRunCalculateButton)
        self.userInterface.RunAdditionalCalculateButton.clicked.connect(self.onClickRunAdditionalCalculateButton)

    def setValidators(self):
        self.doubleValidator = QtGui.QDoubleValidator()
        self.userInterface.RodLengthLineEdit.setValidator(self.doubleValidator)
        self.userInterface.TimeLineEdit.setValidator(self.doubleValidator)
        self.userInterface.LengthStepLineEdit.setValidator(self.doubleValidator)
        self.userInterface.TimeStepLineEdit.setValidator(self.doubleValidator)
        self.userInterface.BZeroLineEdit.setValidator(self.doubleValidator)
        self.userInterface.BFirtsLineEdit.setValidator(self.doubleValidator)
        self.userInterface.BSecondLineEdit.setValidator(self.doubleValidator)
        self.userInterface.PhiFirstLineEdit.setValidator(self.doubleValidator)
        self.userInterface.PhiSecondLineEdit.setValidator(self.doubleValidator)
    
    def onClickClearSheduleButton(self):
        self.resultSolution = None
        pyplot.gcf().clear()
        self.canvas.draw()

    def onClickRunCalculateButton(self):
        if(not self.fillDataContext()): return

        k = self.dataContext.timeStep / (self.dataContext.lengthStep * self.dataContext.lengthStep) + 0.00000000001
        if (k < 0.25): 
            self.resultSolution = Solution(self.dataContext)
            self.drawShedule(self.resultSolution)
        else: ShowErorMassageBox("Шаги по длине и по времени не удовлетворяют условию устойчивости:\nτ/(h*h) < 1/4")

    def onClickRunAdditionalCalculateButton(self):
        if(self.resultSolution == None):
            ShowErorMassageBox("Дополнительное решение нельзя вывести, так как холст пуст!")
            return
        
        pyplot.plot(self.resultSolution[0], self.resultSolution[3], 'g')
        self.canvas.draw()
    
    def drawShedule(self, data):
        pyplot.gcf().clear()
        self.canvas.draw()

        pyplot.grid()
        pyplot.xlabel("Длина стержня")
        pyplot.ylabel("Время")
        pyplot.plot(data[0], data[1], 'b')
        pyplot.plot(data[0], data[2], 'r')

        self.canvas.draw()

    def fillDataContext(self):
        if self.userInterface.RodLengthLineEdit.text() == "":
            ShowErorMassageBox("Заполните все поля для ввода!")
            return False
        if self.userInterface.TimeLineEdit.text() == "":
            ShowErorMassageBox("Заполните все поля для ввода!")
            return False
        if self.userInterface.LengthStepLineEdit.text() == "":
            ShowErorMassageBox("Заполните все поля для ввода!")
            return False
        if self.userInterface.TimeStepLineEdit.text() == "":
            ShowErorMassageBox("Заполните все поля для ввода!")
            return False
        if self.userInterface.BZeroLineEdit.text() == "":
            ShowErorMassageBox("Заполните все поля для ввода!")
            return False
        if self.userInterface.BFirtsLineEdit.text() == "":
            ShowErorMassageBox("Заполните все поля для ввода!")
            return False
        if self.userInterface.BSecondLineEdit.text() == "":
            ShowErorMassageBox("Заполните все поля для ввода!")
            return False
        if self.userInterface.PhiFirstLineEdit.text() == "":
            ShowErorMassageBox("Заполните все поля для ввода!")
            return False
        if self.userInterface.PhiSecondLineEdit.text() == "":
            ShowErorMassageBox("Заполните все поля для ввода!")
            return False
        
        self.dataContext.initialize(
            float(self.userInterface.RodLengthLineEdit.text().replace(',','.')),
            float(self.userInterface.TimeLineEdit.text().replace(',','.')),
            float(self.userInterface.LengthStepLineEdit.text().replace(',','.')),
            float(self.userInterface.TimeStepLineEdit.text().replace(',','.')),
            float(self.userInterface.BZeroLineEdit.text().replace(',','.')),
            float(self.userInterface.BFirtsLineEdit.text().replace(',','.')),
            float(self.userInterface.BSecondLineEdit.text().replace(',','.')),
            float(self.userInterface.PhiFirstLineEdit.text().replace(',','.')),
            float(self.userInterface.PhiSecondLineEdit.text().replace(',','.'))
        )

        return True