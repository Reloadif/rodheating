from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

import sys, os, os.path

def ShowErorMassageBox(text):
    msg = QMessageBox()
    msg.setWindowTitle("Ошибка")
    icondir = ""
    if hasattr(sys, "_MEIPASS"): icondir = os.path.join(sys._MEIPASS, './icons/warning.png')
    else: icondir = './icons/warning.png'
    msg.setWindowIcon(QIcon(icondir))
    msg.setInformativeText(text)
    msg.setStyleSheet("min-width: 200px;")
    msg.exec_()

def ShowInformationMassageBox(text):
    msg = QMessageBox()
    msg.setWindowTitle("Информация")
    icondir = ""
    if hasattr(sys, "_MEIPASS"): icondir = os.path.join(sys._MEIPASS, './icons/info.png')
    else: icondir = './icons/info.png'
    msg.setWindowIcon(QIcon(icondir))
    msg.setInformativeText(text)
    msg.setStyleSheet("min-width: 200px;")
    msg.exec_()

class DataContext:
    def __init__(self):
        self.initialized = False

        self.rodLength = None
        self.time = None
        self.lengthStep = None
        self.timeStep = None
        self.b0 = None
        self.b1 = None
        self.b2 = None
        self.phi1 = None
        self.phi2 = None
    
    def initialize(self, rodLength, time, lengthStep, timeStep, b0, b1, b2, phi1, phi2):
        self.rodLength = rodLength
        self.time = time
        self.lengthStep = lengthStep
        self.timeStep = timeStep
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        self.phi1 = phi1
        self.phi2 = phi2

        self.initialized = True

from math import cos, pi
from tqdm import tqdm

def functionPhi(x, l, phi1, phi2):
    return 1 / l + phi1 * cos((pi * x) / l) + phi2 * cos(2 * (pi * x) / l)

def functionB(x, l, b0, b1, b2):
    return b0 + b1 * cos((pi * x) / l) + b2 * cos(2 * (pi * x) / l)

# Функция численного интегрирования
def SimpsonIntegration(h, customFunction):
    result = (h / 3) * (customFunction[0] + customFunction[len(customFunction) - 1])

    for i in range(1, len(customFunction) - 1, 2):
        result += (h / 3) * (4 * customFunction[i] + 2 * customFunction[i + 1])
    return result

# Метод прогонки
def SweepMethod(a, b, c, func, count):
    A = []
    B = []
    result = [0] * count

    A.append(-c[0]/b[0])
    B.append(func[0]/b[0])
    for i in range(1, count):
        A.append(-c[i] / (a[i] * A[i - 1] + b[i]))
        B.append((func[i] - a[i] * B[i - 1]) / (a[i] * A[i - 1] + b[i]))

    result[count-1] = B[count - 1]

    for i in range(count - 2, -1, -1):
        result[i] = (A[i] * result[i + 1] + B[i])
    return result

def Solution(data):
    funcionPhiValue = []
    functionBValue = []
    slicesFirst = [[]]
    slicesSecond = [[]]

    count_N = int(data.rodLength / data.lengthStep)
    count_T = int(data.time / data.timeStep)

    # Вычисление значений функции и заполнение первого слоя сетки
    for i in range(0, count_N):
        funcionPhiValue.append(functionPhi(i * data.lengthStep, data.rodLength, data.phi1, data.phi2))
        functionBValue.append(functionB(i * data.lengthStep, data.rodLength, data.b0, data.b1, data.b2))
        slicesFirst[0].append(funcionPhiValue[i])
        slicesSecond[0].append(funcionPhiValue[i])

    # Заполнение матрицы коэффициентов для метода прогонки
    coefficientA = [0.0]
    coefficientB = [1.0]
    coefficientC = [-1.0]
    for i in range(1, count_N - 1):
        coefficientA.append(data.timeStep / (data.lengthStep * data.lengthStep))
        coefficientB.append(-1 - 2 * data.timeStep / (data.lengthStep * data.lengthStep))
        coefficientC.append(data.timeStep / (data.lengthStep * data.lengthStep))
    coefficientA.append(-1.0)
    coefficientB.append(1.0)
    coefficientC.append(0.0)

    # Вычисление последующих слоев сетки
    for i in range(1, count_T):
        I = SimpsonIntegration(data.lengthStep, functionBValue)
        fu = [0]
        fu2 = [0]
        slicesFirst.append([])
        slicesSecond.append([])

        # Вычисляем правую часть системы для прогонки
        for j in range(1, count_N - 1):
            fu.append(-slicesFirst[i - 1][j] * ((functionBValue[j] - I) * data.timeStep * data.timeStep  + 1.0))
            fu2.append(-slicesSecond[i - 1][j] * (functionBValue[j] * data.timeStep * data.timeStep + 1.0))
        fu.append(0)
        fu2.append(0)

        # Метод прогонки для системы из B
        res = SweepMethod(coefficientA, coefficientB, coefficientC, fu, count_N)
        for j in range(0, count_N):
            slicesFirst[i].append(res[j])

        # Метод прогонки для системы из A
        res2 = SweepMethod(coefficientA, coefficientB, coefficientC, fu2, count_N)
        for j in range(0, count_N):
            slicesSecond[i].append(res2[j])

    I = SimpsonIntegration(data.lengthStep, slicesSecond[count_T - 1])

    resA = []
    resB = []
    for j in range(0, count_N):
        resA.append(slicesSecond[count_T - 1][j] / I)
        resB.append(slicesFirst[count_T - 1][j])

    xValue = []
    for i in range(0, count_N):
        xValue.append(i * data.lengthStep)

    return xValue, funcionPhiValue, slicesFirst[count_T - 1], resA
