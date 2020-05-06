# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


import sys, os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon , QPixmap
import cv2
import numpy as np
import imutils
from collections import deque



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(589, 421)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Button1 = QtWidgets.QPushButton(self.centralwidget)
        self.Button1.setGeometry(QtCore.QRect(340, 300, 91, 31))
        self.Button1.setObjectName("Button1")
        self.Button2 = QtWidgets.QPushButton(self.centralwidget)
        self.Button2.setGeometry(QtCore.QRect(450, 300, 81, 31))
        self.Button2.setObjectName("Button2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 589, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Button1.setText(_translate("MainWindow", "upload vedio"))
        self.Button2.setText(_translate("MainWindow", "goal checking"))
    





class Widget(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self, MainWindow):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(MainWindow)
        self.Button1.clicked.connect(self.openFile)
        self.Button2.clicked.connect(self.imageProcessing)


    def imageProcessing(self, MainWindow):
        greenLower =(25, 100 , 100)
        greenUpper =(46, 255, 255)
        pts = deque(maxlen=20)
        video = cv2.VideoCapture(self.fileName)

        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        out = cv2.VideoWriter('outputt.avi',fourcc, 25.0,(1000,562),True)

        xmin = 1000
        xmin2= 1000
        flag = 1
        flag3 = 1
        final=None
        ##xxx="No Goal"
        while(video.isOpened()):
            flag2= 0
            _, frame = video.read()
            if frame is None:
                break
        #     frame = imutils.rotate(frame, 180)
            frame = imutils.resize(frame, width=1000)
            (h, w) = frame.shape[:2]
            
            
            
            
            #LINE detection  # detect xmin2

            if flag==1:
                frame2=frame.copy()
                hsv = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
                lower_white = np.array([86  , 0 ,129])
                upper_white = np.array([195 , 18, 255])

                mask = cv2.inRange(hsv, lower_white, upper_white)

                kernel = np.ones((4,4), np.uint8)
                mask = cv2.erode(mask, kernel, iterations=1)
                mask = cv2.dilate(mask, kernel, iterations=1)
                #cv2.imshow("mask",mask)

                contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=cv2.contourArea, reverse=True)
                if len(contours) > 0:
                    cv2.drawContours(frame2, [contours[0]], -1, (0, 255, 0), 5)
                    for i in range (0,len(contours[0])):
                        #print(contours[0][i][0][0])
                        if contours[0][i][0][0] < xmin2:
                            xmin2=contours[0][i][0][0]
                    cv2.line(frame2, (xmin2,0),(xmin2,h),(0,0,225),5)
                #cv2.imshow("frame2",frame2)
                flag=0
                
            
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            kernel=np.ones((5,5),np.uint8)
            mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
            mask = cv2.dilate(mask, kernel, iterations=2)
            mask = cv2.erode(mask, kernel, iterations=2)
            res=cv2.bitwise_and(frame,frame,mask=mask)
            cnts,_=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
            #cv2.imshow("mask",mask)
            
            center = None
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                
                if x<xmin and x>50:
                    xmin=x
                    #final=frame.copy()
                    flag2=1
                
                if radius > 70: 
                ##if True :
                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                    if x+radius < xmin2:
                        xxx="Goal"
                    else:
                        xxx="No Goal"

            if (xxx=="No Goal"):
                cv2.putText(frame, "No Goal", (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 6)
            else:
                cv2.putText(frame, "Goal", (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
                
            cv2.line(frame, (xmin2,0),(xmin2,h),(0,0,225),5)
        #     cv2.line(frame,point1,point2,(255,0,0),2)
            if flag2==1:
                final=frame.copy()
            cv2.imshow("Frame", frame)
            #(h, w) = frame.shape[:2]
            #print(h)
            #print(w)
            out.write(frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27:
                break

        if final is not None:
            cv2.imshow("extreme left",final)
            cv2.waitKey()
            cv2.imwrite("final.png",final)

        video.release()
        out.release()
    def openFile(self):   
        self.fileName, _ = QFileDialog.getOpenFileName(self, "upload vedio",".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi *.MOV)")





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Widget(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
