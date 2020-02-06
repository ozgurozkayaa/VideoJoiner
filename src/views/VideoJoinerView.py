# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\VideoJoinerUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

import os
from functools import partial
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog

'''
Class generated by QtDesigner
'''
class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(480, 240)
        MainWindow.setMinimumSize(QtCore.QSize(480, 240))
        MainWindow.setMaximumSize(QtCore.QSize(480, 240))
        MainWindow.setAnimated(True)
        icon_path = os.path.join(os.getcwd(), "images", "256x256.png")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.txtVideoPath = QtWidgets.QLineEdit(self.centralwidget)
        self.txtVideoPath.setGeometry(QtCore.QRect(10, 10, 371, 23))
        self.txtVideoPath.setObjectName("txtVideoPath")
        self.btnSelectVideo = QtWidgets.QPushButton(self.centralwidget)
        self.btnSelectVideo.setGeometry(QtCore.QRect(390, 10, 75, 23))
        self.btnSelectVideo.setObjectName("btnSelectVideo")
        self.btnJoin = QtWidgets.QPushButton(self.centralwidget)
        self.btnJoin.setGeometry(QtCore.QRect(10, 40, 75, 23))
        self.btnJoin.setObjectName("btnJoin")
        self.txtLog = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txtLog.setGeometry(QtCore.QRect(10, 70, 451, 101))
        self.txtLog.setObjectName("txtLog")
        self.txtLog.setReadOnly(True)
        self.btnOpenFolder = QtWidgets.QPushButton(self.centralwidget)
        self.btnOpenFolder.setGeometry(QtCore.QRect(10, 180, 75, 23))
        self.btnOpenFolder.setObjectName("btnOpenFolder")
        self.btnOpenFolder.setEnabled(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Únicos Gaming :: Clips"))
        self.btnSelectVideo.setText(_translate("MainWindow", "Select video"))
        self.btnJoin.setText(_translate("MainWindow", "Join"))
        self.btnOpenFolder.setText(_translate("MainWindow", "Open folder"))


class VideoJoinerView(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, gui, viewmodel, parent=None):
        super().__init__(parent)

        self._viewmodel = viewmodel

        self.setupUi(self)

        self.configure_signals()

        #self.output_path = ''

    def configure_signals(self):
        # GUI signals
        self.btnSelectVideo.clicked.connect(self.open_file_dialog)
        self.btnJoin.clicked.connect(lambda: self._viewmodel.start(self.txtVideoPath.text()))
        self.btnOpenFolder.clicked.connect(self._viewmodel.open_explorer)

        # Viewmodel signals
        self._viewmodel.onLog.connect(self.write_log)
        self._viewmodel.onJobStarted.connect(self.job_started)
        self._viewmodel.onJobFinished.connect(self.job_finished)
        self._viewmodel.onConvertStarted.connect(partial(self.process_started, "Conversion"))
        self._viewmodel.onConvertFinished.connect(partial(self.process_finished, "Conversion"))
        self._viewmodel.onJoinStarted.connect(partial(self.process_started, "Join"))
        self._viewmodel.onJoinFinished.connect(partial(self.process_finished, "Join"))
        # TODO: Subscribe to onJoinOutro
        
        self._viewmodel.onError.connect(self.write_log)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        filename, _ = QFileDialog.getOpenFileName(self, "Select video", "", "MP4 files (*.mp4);; MOV files (*.mov)", options=options)

        if filename:
            self.txtVideoPath.setText(filename)

    def enable_controls(self, isEnable):
        self.txtVideoPath.setEnabled(isEnable)
        self.btnSelectVideo.setEnabled(isEnable)
        self.btnJoin.setEnabled(isEnable)

    @QtCore.pyqtSlot(str)
    def write_log(self, message):
        self.txtLog.appendPlainText(message)

    @QtCore.pyqtSlot()
    def job_started(self):
        self.enable_controls(False)

    @QtCore.pyqtSlot()
    def job_finished(self):
        self.write_log(f"\nClip available on:\n {self._viewmodel.output_path}")
        self.enable_controls(True)
        
        if os.path.exists(self._viewmodel.output_path):
            self.btnOpenFolder.setEnabled(True)

    @QtCore.pyqtSlot(str)
    def process_started(self, value):
        self.write_log(f"Starting {value} process")
    
    @QtCore.pyqtSlot(str)
    def process_finished(self, value):
        self.write_log(f"Process {value} finished")

