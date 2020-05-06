import os
import sys
from PyQt5 import QtWidgets, QtGui


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip('PrntSC Downloader')
        self.activated.connect(self.onTrayIconActivated)
        self.parentWindow = parent

    def onTrayIconActivated(self, reason):
        if reason == self.DoubleClick:
        	self.parentWindow.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("icon.png"), w)
    tray_icon.show()
    tray_icon.showMessage('PrntSc Downloader', 'The application is running, double click to open.')
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()