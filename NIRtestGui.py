# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NIRtest.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(776, 442)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnReadBatVoltage = QtGui.QPushButton(self.centralwidget)
        self.btnReadBatVoltage.setObjectName(_fromUtf8("btnReadBatVoltage"))
        self.gridLayout.addWidget(self.btnReadBatVoltage, 1, 0, 1, 1)
        self.btnLEDtest = QtGui.QPushButton(self.centralwidget)
        self.btnLEDtest.setObjectName(_fromUtf8("btnLEDtest"))
        self.gridLayout.addWidget(self.btnLEDtest, 0, 0, 1, 1)
        self.lnBatteryVoltage = QtGui.QLineEdit(self.centralwidget)
        self.lnBatteryVoltage.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lnBatteryVoltage.setObjectName(_fromUtf8("lnBatteryVoltage"))
        self.gridLayout.addWidget(self.lnBatteryVoltage, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "NIRScan", None))
        self.btnReadBatVoltage.setText(_translate("MainWindow", "Read Battery Voltage", None))
        self.btnLEDtest.setText(_translate("MainWindow", "LED Test", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

