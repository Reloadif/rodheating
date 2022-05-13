from PyQt5.QtWidgets import QApplication

from MainMatplotWindow import MainMatplotWindow

def main():
    application = QApplication([])
    mainWindow = MainMatplotWindow()
    mainWindow.show()
    application.exec()

if __name__ == '__main__':
    main()