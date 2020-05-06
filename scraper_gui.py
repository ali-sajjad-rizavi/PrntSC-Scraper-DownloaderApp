# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newbulk.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from scraper_tray import *


import tkinter as tk

class TkMessageBox:
    def showMessage_InternetDisconnected():
        root = tk.Tk()
        root.title('Internet disconnected!')
        root.resizable(False, False)
        tk.Label(root, text='Close the program and run again to resume.').grid(row=0, pady=15, padx=10)
        tk.Button(root, text="OK", command=lambda: root.destroy()).grid(row=1, pady=10)
        root.mainloop()

    def showMessage_NextSuggestedRange(msg):
        root = tk.Tk()
        root.title('Success!')
        root.resizable(False, False)
        tk.Label(root, text=msg).grid(row=0, padx=10, pady=10)
        tk.Button(root, text='OK', command=lambda: root.destroy()).grid(row=1, pady=10)
        root.mainloop()



class Ui_MainWindow(object):
    def setupUi(self, MainWindow, application):
        self.mainWindowHandle = MainWindow
        self.applicationHandle = application
        self.Tray = SystemTrayIcon(QtGui.QIcon("robot.ico"), MainWindow)
        #--------------------------------------
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(545, 415)
        MainWindow.setWindowIcon(QtGui.QIcon('robot.ico'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.browse_Button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_Button.setGeometry(QtCore.QRect(418, 180, 75, 23))
        self.browse_Button.setObjectName("browse_Button")
        self.browse_Button.clicked.connect(self.__showFolderBrowseDialog)
        #---------------------------------------------------------
        self.startDownloader_Button = QtWidgets.QPushButton(self.centralwidget)
        self.startDownloader_Button.setGeometry(QtCore.QRect(70, 250, 111, 51))
        self.startDownloader_Button.setObjectName("startDownloader_Button")
        self.startDownloader_Button.clicked.connect(self.applicationHandle.start_DownloaderThread)
        #-----------------------------------------------------------------
        self.endNumber_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.endNumber_lineEdit.setGeometry(QtCore.QRect(310, 60, 81, 20))
        self.endNumber_lineEdit.setObjectName("endNumber_lineEdit")
        self.endNumber_lineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[0-9]+'), self.mainWindowHandle))
        #---------------------------------------------------------------------
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 60, 41, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(280, 60, 31, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.startNumber_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.startNumber_lineEdit.setGeometry(QtCore.QRect(180, 60, 81, 20))
        self.startNumber_lineEdit.setObjectName("startNumber_lineEdit")
        self.startNumber_lineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[0-9]+'), self.mainWindowHandle))
        #-----------------------------------------------------------------------
        self.dirpath_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.dirpath_lineEdit.setEnabled(False)
        self.dirpath_lineEdit.setGeometry(QtCore.QRect(150, 180, 261, 20))
        self.dirpath_lineEdit.setReadOnly(False)
        self.dirpath_lineEdit.setObjectName("dirpath_lineEdit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 180, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(200, 260, 301, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        self.status_label.setFont(font)
        self.status_label.setObjectName("status_label")
        self.downloadedCount_label = QtWidgets.QLabel(self.centralwidget)
        self.downloadedCount_label.setGeometry(QtCore.QRect(40, 360, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        self.downloadedCount_label.setFont(font)
        self.downloadedCount_label.setObjectName("downloadedCount_label")
        self.remainingCount_label = QtWidgets.QLabel(self.centralwidget)
        self.remainingCount_label.setGeometry(QtCore.QRect(340, 360, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        self.remainingCount_label.setFont(font)
        self.remainingCount_label.setObjectName("remainingCount_label")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(240, 110, 111, 41))
        self.dateEdit.setObjectName("dateEdit")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(80, 120, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.minimizeToTray_Button = QtWidgets.QPushButton(self.centralwidget)
        self.minimizeToTray_Button.setGeometry(QtCore.QRect(454, 0, 91, 23))
        self.minimizeToTray_Button.setObjectName("minimizeToTray_Button")
        self.minimizeToTray_Button.clicked.connect(self.__minimize_MainWindow_toTray)
        #---------------------------------------------------------------------------
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PrntSc Downloader"))
        self.browse_Button.setText(_translate("MainWindow", "Browse"))
        self.startDownloader_Button.setText(_translate("MainWindow", "Start Downloader"))
        self.endNumber_lineEdit.setText(_translate("MainWindow", "2176782335"))
        self.label.setText(_translate("MainWindow", "From:"))
        self.label_2.setText(_translate("MainWindow", "To:"))
        self.startNumber_lineEdit.setText(_translate("MainWindow", "0"))
        self.label_3.setText(_translate("MainWindow", "Select folder:"))
        self.status_label.setText(_translate("MainWindow", "Status: N/A"))
        self.downloadedCount_label.setText(_translate("MainWindow", "Downloaded: N/A"))
        self.remainingCount_label.setText(_translate("MainWindow", "Remaining: N/A"))
        self.label_7.setText(_translate("MainWindow", "Min. Last Modified Date:"))
        self.minimizeToTray_Button.setText(_translate("MainWindow", "Minimize to Tray"))

    #----------------------------------------------------------------------------------------------
    def __minimize_MainWindow_toTray(self):
        self.Tray.show()
        self.mainWindowHandle.hide()
        self.Tray.showMessage('PrntSc Downloader', 'The application is running, double click to open.')

    def __showFolderBrowseDialog(self):
        self.dirpath_lineEdit.setText(str(QtWidgets.QFileDialog.getExistingDirectory(self.mainWindowHandle, "Select Directory")))

    def setResumeCapability(self):
        import os
        if os.path.isfile('resumeinfo.csv') == False:
            return
        with open('resumeinfo.csv', 'r') as resumeinfo_file:
            info_list = resumeinfo_file.readline().strip().split(',')
            self.startNumber_lineEdit.setText(info_list[0])
            self.endNumber_lineEdit.setText(info_list[1])
            self.dateEdit.setDate(QtCore.QDate().fromString(info_list[2]))
            self.dirpath_lineEdit.setText(info_list[3])
            self.applicationHandle.folder_count = int(info_list[4])
        msg = QtWidgets.QMessageBox(self.mainWindowHandle)
        msg.setText('Values have been set from the previous incomplete task. Press Start Download to resume.')
        msg.setWindowTitle('Resume previous task!')
        msg.setWindowIcon(QtGui.QIcon('robot.ico'))
        msg.exec_()

    def setNext_SuggestedRange(self, start_lineNo):
        if start_lineNo > 2176782335:
            msg = 'Task completed successfully!'
        else:
            msg = 'Task completed! Next suggested range has been set. Press Start Download to continue.'
            self.startNumber_lineEdit.setText(str(start_lineNo))
            if 2176782335 - start_lineNo < 1000:
                self.endNumber_lineEdit.setText(str(2176782335))
            else:
                self.endNumber_lineEdit.setText(str(start_lineNo + 1000))
            self.startDownloader_Button.setEnabled(True)
        TkMessageBox.showMessage_NextSuggestedRange(msg)

    def showInternetConnectionError(self):
        TkMessageBox.showMessage_InternetDisconnected()

#=====================================================

class Form(QtWidgets.QMainWindow):
    def __init__(self, application):
        QtWidgets.QMainWindow.__init__(self)
        self.applicationHandle = application

    def closeEvent(self, event):
        self.applicationHandle.is_window_closed = True
        if self.applicationHandle.downloader_thread.is_alive():
            self.applicationHandle.downloader_thread.join()
        event.accept()

#--------#
##-MAIN-##
#--------#


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Form()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())