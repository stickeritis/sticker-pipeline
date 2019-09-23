# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visualizer_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VisualizerWindow(object):
    def setupUi(self, VisualizerWindow):
        VisualizerWindow.setObjectName("VisualizerWindow")
        VisualizerWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(VisualizerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.inputTextEdit = QtWidgets.QPlainTextEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputTextEdit.sizePolicy().hasHeightForWidth())
        self.inputTextEdit.setSizePolicy(sizePolicy)
        self.inputTextEdit.setObjectName("inputTextEdit")
        self.horizontalLayout.addWidget(self.inputTextEdit)
        self.processButton = QtWidgets.QPushButton(self.groupBox)
        self.processButton.setObjectName("processButton")
        self.horizontalLayout.addWidget(self.processButton)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.annotationsWebView = QtWebEngineWidgets.QWebEngineView(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.annotationsWebView.sizePolicy().hasHeightForWidth())
        self.annotationsWebView.setSizePolicy(sizePolicy)
        self.annotationsWebView.setMinimumSize(QtCore.QSize(0, 400))
        self.annotationsWebView.setObjectName("annotationsWebView")
        self.horizontalLayout_2.addWidget(self.annotationsWebView)
        self.verticalLayout.addWidget(self.groupBox_2)
        VisualizerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(VisualizerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        VisualizerWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(VisualizerWindow)
        self.statusbar.setObjectName("statusbar")
        VisualizerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(VisualizerWindow)
        QtCore.QMetaObject.connectSlotsByName(VisualizerWindow)

    def retranslateUi(self, VisualizerWindow):
        _translate = QtCore.QCoreApplication.translate
        VisualizerWindow.setWindowTitle(_translate("VisualizerWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("VisualizerWindow", "Parse"))
        self.processButton.setText(_translate("VisualizerWindow", "Process"))
        self.groupBox_2.setTitle(_translate("VisualizerWindow", "Annotations"))
from PyQt5 import QtWebEngineWidgets
