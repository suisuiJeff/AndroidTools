#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/6/5
Desc  : copyFile widget
"""

from PyQt4 import QtGui, QtCore
from util.EncodeUtil import _fromUtf8
from util.RunSysCommand import RunSysCommand
from util import FileUtil
import re
import os


class CopyFileWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self._runSysCmd = RunSysCommand()
        mainLayout = QtGui.QVBoxLayout()
        operBtnsLayout = QtGui.QHBoxLayout()
        filePathForm = QtGui.QFormLayout()

        srcFilePathLabel = QtGui.QLabel(_fromUtf8("源根目录："))
        destFilePathLabel = QtGui.QLabel(_fromUtf8("目标目录："))
        fileListLabel = QtGui.QLabel(_fromUtf8("文件集合："))
        self.tipsLabel = QtGui.QLabel()
        self.srcFilePathEdit = QtGui.QLineEdit()
        self.destFilePathEdit = QtGui.QLineEdit()
        self.fileListEdit = QtGui.QTextEdit()
        srcFilePathLabel.setMinimumHeight(25)
        destFilePathLabel.setMinimumHeight(25)
        self.srcFilePathEdit.setMinimumHeight(25)
        self.destFilePathEdit.setMinimumHeight(25)

        self.srcFilePathEdit.setPlaceholderText(_fromUtf8("Y:\work_src\gitlab\I13\HLOS"))
        self.destFilePathEdit.setPlaceholderText(_fromUtf8("G:\copyfile"))

        self.copyFileBtn = QtGui.QPushButton(u'拷贝文件')
        self.deleteDirBtn = QtGui.QPushButton(u'删除目录')
        self.startFileBtn = QtGui.QPushButton(u'打开文件')
        self.copyFileBtn.setFixedSize(100, 30)
        self.deleteDirBtn.setFixedSize(100, 30)
        self.startFileBtn.setFixedSize(100, 30)
        self.copyFileBtn.connect(self.copyFileBtn, QtCore.SIGNAL('clicked()'), self.copyFileBtnClick)
        self.deleteDirBtn.connect(self.deleteDirBtn, QtCore.SIGNAL('clicked()'), self.deleteDirBtnClick)
        self.startFileBtn.connect(self.startFileBtn, QtCore.SIGNAL('clicked()'), self.startFileBtnClick)

        filePathForm.addRow(srcFilePathLabel, self.srcFilePathEdit)
        filePathForm.addRow(destFilePathLabel, self.destFilePathEdit)
        filePathForm.addRow(fileListLabel, self.fileListEdit)
        # 将表单最后一个文本框设置为可垂直拉伸 QtGui.QSizePolicy
        policy = self.fileListEdit.sizePolicy()
        policy.setVerticalStretch(1)
        self.fileListEdit.setSizePolicy(policy)

        operBtnsLayout.addWidget(self.tipsLabel)
        operBtnsLayout.addStretch(1)
        operBtnsLayout.addWidget(self.copyFileBtn)
        operBtnsLayout.addWidget(self.deleteDirBtn)
        operBtnsLayout.addWidget(self.startFileBtn)
        mainLayout.addLayout(filePathForm)
        mainLayout.addLayout(operBtnsLayout)
        self.setLayout(mainLayout)

    # copy file
    def copyFileBtnClick(self):
        srcFilePath = unicode(self.srcFilePathEdit.text())
        destFilePath = unicode(self.destFilePathEdit.text())
        fileListEdit = str(self.fileListEdit.toPlainText())
        if not fileListEdit:
            tips = unicode("请在文件集合框中输入拷贝文件路径")
            self.setTips(_fromUtf8(tips))
            return
        srcFilePath = (srcFilePath if srcFilePath.strip() else str("Y:\\work_src\\gitlab\\I13\\HLOS"))
        destFilePath = (destFilePath if destFilePath.strip() else str("G:\\copyfile"))
        FileUtil.mkdirNotExist(destFilePath)
        # print fileListEdit
        # .* 匹配除换行符 \n 之外的任何字符 \S 匹配任何非空白字符, 此处用来匹配保存在string中的文件目录格式
        reFileStr = r'(.*\S)'
        fileList = re.findall(reFileStr, fileListEdit)
        if not fileList:
            tips = unicode("没有在文件集合中找到文件路径")
            self.setTips(_fromUtf8(tips))
            return
        for fileName in fileList:
            if not fileName:
                continue
            if fileName.startswith("/") or fileName.startswith("\\"):
                fileName = fileName[1:]
            fileName = fileName.replace("/", "\\")
            # srcFile = os.path.join(srcFilePath, fileName)
            # destFile = os.path.join(destFilePath, fileName)
            # print 'srcFilePath: ', srcFile
            # print 'destFile: ', destFile
            FileUtil.copyFile(srcFilePath, destFilePath,srcFilePath, fileName)
        tips = unicode("拷贝完成: ") + destFilePath
        self.setTips(_fromUtf8(tips))
        self._runSysCmd.run(['explorer.exe', destFilePath])

    def deleteDirBtnClick(self):
        destFilePath = unicode(self.destFilePathEdit.text())
        destFilePath = (destFilePath if destFilePath.strip() else str("G:\\copyfile"))
        FileUtil.removeDirs(destFilePath)

    def startFileBtnClick(self):
        srcFilePath = unicode(self.srcFilePathEdit.text())
        if srcFilePath and not srcFilePath.startswith(u'Y:\work_src\gitlab'):
            if srcFilePath.startswith("\\") or srcFilePath.startswith("/"):
                i13dir = str("Y:\\work_src\\gitlab\\I13\HLOS")
            else:
                i13dir = str("Y:\\work_src\\gitlab\\I13\HLOS\\")
            srcFilePath = i13dir + srcFilePath
        srcFilePath = srcFilePath.replace('/', '\\')
        print srcFilePath
        self._runSysCmd.run(['explorer.exe', srcFilePath])

    def setTips(self, text):
        self.tipsLabel.setText(text)

