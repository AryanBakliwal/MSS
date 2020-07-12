# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mslib/msui/ui/ui_mscolab_project_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MscolabProject(object):
    def setupUi(self, MscolabProject):
        MscolabProject.setObjectName("MscolabProject")
        MscolabProject.setWindowModality(QtCore.Qt.NonModal)
        MscolabProject.setEnabled(True)
        MscolabProject.resize(867, 687)
        MscolabProject.setMinimumSize(QtCore.QSize(600, 400))
        self.centralwidget = QtWidgets.QWidget(MscolabProject)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.user_info = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.user_info.sizePolicy().hasHeightForWidth())
        self.user_info.setSizePolicy(sizePolicy)
        self.user_info.setObjectName("user_info")
        self.horizontalLayout_3.addWidget(self.user_info)
        self.proj_info = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.proj_info.sizePolicy().hasHeightForWidth())
        self.proj_info.setSizePolicy(sizePolicy)
        self.proj_info.setObjectName("proj_info")
        self.horizontalLayout_3.addWidget(self.proj_info)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.collaboratorsList = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.collaboratorsList.sizePolicy().hasHeightForWidth())
        self.collaboratorsList.setSizePolicy(sizePolicy)
        self.collaboratorsList.setMinimumSize(QtCore.QSize(256, 300))
        self.collaboratorsList.setObjectName("collaboratorsList")
        self.horizontalLayout_4.addWidget(self.collaboratorsList)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.messageList = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messageList.sizePolicy().hasHeightForWidth())
        self.messageList.setSizePolicy(sizePolicy)
        self.messageList.setMinimumSize(QtCore.QSize(539, 300))
        self.messageList.setObjectName("messageList")
        self.verticalLayout_3.addWidget(self.messageList)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.previewBtn = QtWidgets.QPushButton(self.centralwidget)
        self.previewBtn.setAutoDefault(False)
        self.previewBtn.setDefault(False)
        self.previewBtn.setFlat(False)
        self.previewBtn.setObjectName("previewBtn")
        self.horizontalLayout_2.addWidget(self.previewBtn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.messageTextContainer = QtWidgets.QWidget(self.centralwidget)
        self.messageTextContainer.setObjectName("messageTextContainer")
        self.horizontalLayout.addWidget(self.messageTextContainer)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.sendMessageBtn = QtWidgets.QPushButton(self.centralwidget)
        self.sendMessageBtn.setDefault(True)
        self.sendMessageBtn.setObjectName("sendMessageBtn")
        self.verticalLayout.addWidget(self.sendMessageBtn)
        self.uploadBtn = QtWidgets.QPushButton(self.centralwidget)
        self.uploadBtn.setObjectName("uploadBtn")
        self.verticalLayout.addWidget(self.uploadBtn)
        self.editMessageBtn = QtWidgets.QPushButton(self.centralwidget)
        self.editMessageBtn.setObjectName("editMessageBtn")
        self.verticalLayout.addWidget(self.editMessageBtn)
        self.cancelBtn = QtWidgets.QPushButton(self.centralwidget)
        self.cancelBtn.setEnabled(True)
        self.cancelBtn.setObjectName("cancelBtn")
        self.verticalLayout.addWidget(self.cancelBtn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.setStretch(0, 4)
        self.verticalLayout_3.setStretch(1, 1)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        MscolabProject.setCentralWidget(self.centralwidget)
        self.actionCloseWindow = QtWidgets.QAction(MscolabProject)
        self.actionCloseWindow.setObjectName("actionCloseWindow")
        MscolabProject.addAction(self.actionCloseWindow)

        self.retranslateUi(MscolabProject)
        self.actionCloseWindow.triggered.connect(MscolabProject.close)
        QtCore.QMetaObject.connectSlotsByName(MscolabProject)

    def retranslateUi(self, MscolabProject):
        _translate = QtCore.QCoreApplication.translate
        MscolabProject.setWindowTitle(_translate("MscolabProject", "Mscolab Project Chat"))
        self.user_info.setText(_translate("MscolabProject", "Logged In: "))
        self.proj_info.setText(_translate("MscolabProject", "Project:"))
        self.previewBtn.setText(_translate("MscolabProject", "Preview"))
        self.sendMessageBtn.setText(_translate("MscolabProject", "send"))
        self.uploadBtn.setText(_translate("MscolabProject", "Upload"))
        self.editMessageBtn.setText(_translate("MscolabProject", "Update"))
        self.cancelBtn.setText(_translate("MscolabProject", "Cancel"))
        self.actionCloseWindow.setText(_translate("MscolabProject", "CloseWindow"))
        self.actionCloseWindow.setShortcut(_translate("MscolabProject", "Ctrl+W"))

