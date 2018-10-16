#工科创2B前端代码
#
#Author: 郭远帆
#rev.0 2018.10.15

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import sys
import numpy as np
class Ui_Form(QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__()
        #设置主窗口
        self.setupUi()
        #相机设置
        self.timer_camera = QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 1
        #设置信号槽
        self.slot_init()
        #设置下拉菜单
        self.initMenu()
        self.initAnimation()
        self.GrayFlag = False
        self.TwoValueFlag =False
    def setupUi(self):
        self.resize(1050, 800)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 391, 381))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.OriginFaceLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.OriginFaceLayout.setContentsMargins(0, 0, 0, 0)
        self.OriginFaceLayout.setObjectName("OriginFaceLayout")
        self.OriginalImgLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.OriginalImgLabel.setObjectName("OriginalImgLabel")
        self.OriginFaceLayout.addWidget(self.OriginalImgLabel)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(480, 10, 391, 381))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.GrayLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.GrayLayout.setContentsMargins(0, 0, 0, 0)
        self.GrayLayout.setObjectName("GrayLayout")
        self.GrayLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.GrayLabel.setObjectName("GrayLabel")
        self.GrayLayout.addWidget(self.GrayLabel)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 400, 391, 381))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.TwoValueLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.TwoValueLayout.setContentsMargins(0, 0, 0, 0)
        self.TwoValueLayout.setObjectName("TwoValueLayout")
        self.TwoValueLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.TwoValueLabel.setObjectName("TwoValueLabel")
        self.TwoValueLayout.addWidget(self.TwoValueLabel)

        self.setWindowTitle('工科创2B前端')


    #定义信号槽
    def slot_init(self):

        self.timer_camera.timeout.connect(self.show_camera)



    def initAnimation(self):
        # 按钮动画
        self._animation = QPropertyAnimation(
            self._contextMenu, b'geometry', self,
            easingCurve=QEasingCurve.Linear, duration=300)
    def contextMenuEvent(self, event):
        pos = event.globalPos()
        size = self._contextMenu.sizeHint()
        x, y, w, h = pos.x(), pos.y(), size.width(), size.height()
        self._animation.stop()
        self._animation.setStartValue(QRect(x, y, 0, 0))
        self._animation.setEndValue(QRect(x, y, w, h))
        self._animation.start()
        self._contextMenu.exec_(event.globalPos())

    def initMenu(self):
        self._contextMenu = QMenu(self)
        self.ac_open_cama = self._contextMenu.addAction('打开相机', self.CameraOperation)
        self.ac_gray= self._contextMenu.addAction('查看灰度图', self.Grayon)
        self.ac_TwoValue = self._contextMenu.addAction('查看二值化图',self.TwoValueOn)

    #打开相机操作
    def CameraOperation(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"Please check you have connected your camera",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)

            else:
                self.timer_camera.start(50)
                self.ac_open_cama.setText('关闭相机')
        else:
            self.GrayFlag = True
            self.TwoValueFlag = True
            self.Grayon()
            self.TwoValueOn()
            self.timer_camera.stop()
            self.cap.release()
            self.OriginalImgLabel.clear()
            self.ac_open_cama.setText('打开相机')

    #打开查看灰度图
    def Grayon(self):
        if self.GrayFlag == False:
            self.GrayFlag = True
            self.ac_gray.setText('关闭灰度显示')
        else:
            self.GrayFlag = False
            self.GrayLabel.clear()
            self.ac_gray.setText('开启灰度显示')
    #查看二值化图像
    def TwoValueOn(self):
        if self.TwoValueFlag == False:
            self.TwoValueFlag = True
            self.ac_TwoValue.setText('关闭二值化显示')
        else:
            self.TwoValueFlag = False
            self.TwoValueLabel.clear()
            self.ac_TwoValue.setText('开启二值化显示')
    #摄像头显示函数
    def show_camera(self):
        #读取摄像头信息，显示原图像
        flag, self.image= self.cap.read()

        show = cv2.resize(self.image, (380, 400))
        if self.GrayFlag ==True:
            Gray_show = cv2.cvtColor(show,cv2.COLOR_BGR2GRAY)
            if self.TwoValueFlag ==True:
                #二值化处理
                Two_show = Gray_show.copy()
                Two_show[Two_show>127] = 255
                Two_show[Two_show<=127] = 0
                Two_showImage = QImage(Two_show.data,Two_show.shape[1],Two_show.shape[0],QImage.Format_Grayscale8)
                self.TwoValueLabel.setPixmap(QPixmap.fromImage(Two_showImage))
            Gray_showImage = QImage(Gray_show.data, Gray_show.shape[1],Gray_show.shape[0],QImage.Format_Grayscale8)
            self.GrayLabel.setPixmap(QPixmap.fromImage(Gray_showImage))


        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)

        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],QImage.Format_RGB888)

        self.OriginalImgLabel.setPixmap(QtGui.QPixmap.fromImage(showImage))


app = QtWidgets.QApplication(sys.argv)
ui = Ui_Form()
ui.show()
sys.exit(app.exec_())