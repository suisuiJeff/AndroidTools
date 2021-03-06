#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/2/22
Desc  : adb tool view
"""
from PyQt4 import QtGui, QtCore
from widget.OtherToolsWidget import OtherToolsWidget


class OtherToolsView(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        mainLayout = QtGui.QVBoxLayout()
        self.otherToolsWidget = OtherToolsWidget()

        mainLayout.addWidget(self.otherToolsWidget)
        self.setLayout(mainLayout)

    def setWinWTSMonitor(self, wtsMonitor):
        self.otherToolsWidget.setWinWTSMonitor(wtsMonitor)
