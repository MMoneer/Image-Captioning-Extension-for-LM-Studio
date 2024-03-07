# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'captioning.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLCDNumber, QLabel,
    QLineEdit, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QSize(1200, 800))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMaximumSize(QSize(1200, 800))
        self.centralwidget.setStyleSheet(u"")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 1200, 280))
        self.frame.setStyleSheet(u"color: rgb(224, 224, 224);\n"
"background-color: qlineargradient(spread:pad, x1:0.41405, y1:0.7, x2:0.430939, y2:0.148, stop:0 rgba(53, 65, 83, 255), stop:1 rgba(13, 27, 42, 255));")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(80, 50, 190, 30))
        font = QFont()
        font.setFamilies([u"Roboto Slab SemiBold"])
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(80, 100, 190, 30))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.lineEdit_folder_path = QLineEdit(self.frame)
        self.lineEdit_folder_path.setObjectName(u"lineEdit_folder_path")
        self.lineEdit_folder_path.setGeometry(QRect(309, 50, 621, 30))
        font1 = QFont()
        font1.setPointSize(14)
        self.lineEdit_folder_path.setFont(font1)
        self.lineEdit_folder_path.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.lineEdit_caption_path = QLineEdit(self.frame)
        self.lineEdit_caption_path.setObjectName(u"lineEdit_caption_path")
        self.lineEdit_caption_path.setGeometry(QRect(309, 100, 621, 30))
        self.lineEdit_caption_path.setFont(font1)
        self.lineEdit_caption_path.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.folder_path_pt = QPushButton(self.frame)
        self.folder_path_pt.setObjectName(u"folder_path_pt")
        self.folder_path_pt.setGeometry(QRect(1000, 50, 120, 30))
        font2 = QFont()
        font2.setFamilies([u"Roboto Slab SemiBold"])
        font2.setPointSize(14)
        font2.setBold(True)
        self.folder_path_pt.setFont(font2)
        self.folder_path_pt.setStyleSheet(u"background-color: rgb(53, 65, 83);")
        self.caption_dest_pt = QPushButton(self.frame)
        self.caption_dest_pt.setObjectName(u"caption_dest_pt")
        self.caption_dest_pt.setGeometry(QRect(1000, 100, 120, 30))
        self.caption_dest_pt.setFont(font2)
        self.caption_dest_pt.setStyleSheet(u"background-color: rgb(53, 65, 83);")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(80, 180, 131, 30))
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.run_cation_pt = QPushButton(self.frame)
        self.run_cation_pt.setObjectName(u"run_cation_pt")
        self.run_cation_pt.setGeometry(QRect(520, 175, 160, 40))
        font3 = QFont()
        font3.setFamilies([u"Roboto Slab SemiBold"])
        font3.setPointSize(13)
        font3.setBold(True)
        self.run_cation_pt.setFont(font3)
        self.run_cation_pt.setStyleSheet(u"background-color: rgb(0, 178, 202);\n"
"color: rgb(0, 85, 107);\n"
"")
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(900, 180, 131, 30))
        self.label_5.setFont(font2)
        self.label_5.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.label_server_status = QLabel(self.frame)
        self.label_server_status.setObjectName(u"label_server_status")
        self.label_server_status.setGeometry(QRect(1040, 180, 131, 30))
        self.label_server_status.setFont(font2)
        self.label_server_status.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255, 0, 0);")
        self.progressBar = QProgressBar(self.frame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(20, 245, 1160, 30))
        font4 = QFont()
        font4.setPointSize(14)
        font4.setBold(True)
        self.progressBar.setFont(font4)
        self.progressBar.setStyleSheet(u"")
        self.progressBar.setValue(0)
        self.progressBar.setInvertedAppearance(False)
        self.info_pt = QPushButton(self.frame)
        self.info_pt.setObjectName(u"info_pt")
        self.info_pt.setGeometry(QRect(20, 10, 41, 30))
        font5 = QFont()
        font5.setFamilies([u"Roboto"])
        font5.setPointSize(10)
        font5.setBold(True)
        self.info_pt.setFont(font5)
        self.lcdNumber = QLCDNumber(self.frame)
        self.lcdNumber.setObjectName(u"lcdNumber")
        self.lcdNumber.setGeometry(QRect(220, 180, 81, 30))
        font6 = QFont()
        font6.setPointSize(12)
        font6.setBold(False)
        self.lcdNumber.setFont(font6)
        self.lcdNumber.setLayoutDirection(Qt.LeftToRight)
        self.lcdNumber.setStyleSheet(u"background-color: rgb(0, 178, 202);\n"
"color: rgb(0, 85, 107);")
        self.lcdNumber.setFrameShape(QFrame.NoFrame)
        self.lcdNumber.setFrameShadow(QFrame.Sunken)
        self.lcdNumber.setLineWidth(1)
        self.lcdNumber.setMidLineWidth(2)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setDigitCount(4)
        self.lcdNumber.setMode(QLCDNumber.Dec)
        self.lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber.setProperty("intValue", 0)
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(0, 280, 1200, 520))
        self.frame_2.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.497238, y1:0, x2:0.502762, y2:0.716, stop:0 rgba(53, 65, 83, 255), stop:1 rgba(71, 84, 103, 255));\n"
"color: rgb(236, 236, 236);")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.textEdit = QTextEdit(self.frame_2)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(20, 20, 1160, 480))
        font7 = QFont()
        font7.setFamilies([u"Roboto"])
        font7.setPointSize(14)
        font7.setBold(False)
        self.textEdit.setFont(font7)
        self.textEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"")
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setFrameShadow(QFrame.Raised)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Images Captioning Extension", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Images Folder Path:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Caption Destination:", None))
        self.folder_path_pt.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.caption_dest_pt.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Images Count :", None))
        self.run_cation_pt.setText(QCoreApplication.translate("MainWindow", u"Run Captioning", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Server Status:", None))
        self.label_server_status.setText(QCoreApplication.translate("MainWindow", u"Not Connected", None))
        self.info_pt.setText(QCoreApplication.translate("MainWindow", u"INFO", None))
    # retranslateUi

