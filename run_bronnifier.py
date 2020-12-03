from PyQt5 import QtCore, QtGui, QtWidgets
import qimage2ndarray
import numpy as np
import bronnify


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pic = QtWidgets.QLabel(self.centralwidget)
        self.pic.setGeometry(QtCore.QRect(0, 0, 801, 371))
        self.pic.setText("")
        self.pic.setPixmap(QtGui.QPixmap("this_is_paradise.jpg"))
        self.pic.setScaledContents(True)
        self.pic.setAlignment(QtCore.Qt.AlignCenter)
        self.pic.setObjectName("pic")
        self.Save = QtWidgets.QPushButton(self.centralwidget)
        self.Save.setGeometry(QtCore.QRect(660, 470, 141, 81))
        self.Save.setObjectName("Save")
        self.Open = QtWidgets.QPushButton(self.centralwidget)
        self.Open.setGeometry(QtCore.QRect(660, 380, 141, 81))
        self.Open.setObjectName("Open")
        self.x_slider = QtWidgets.QSlider(self.centralwidget)
        self.x_slider.setGeometry(QtCore.QRect(90, 410, 521, 21))
        self.x_slider.setMinimum(-100)
        self.x_slider.setMaximum(100)
        self.x_slider.setOrientation(QtCore.Qt.Horizontal)
        self.x_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.x_slider.setTickInterval(10)
        self.x_slider.setObjectName("x_slider")
        self.x_crop = QtWidgets.QLabel(self.centralwidget)
        self.x_crop.setGeometry(QtCore.QRect(90, 380, 101, 16))
        self.x_crop.setObjectName("x_crop")
        self.y_slider = QtWidgets.QSlider(self.centralwidget)
        self.y_slider.setGeometry(QtCore.QRect(90, 490, 521, 21))
        self.y_slider.setMinimum(-100)
        self.y_slider.setMaximum(100)
        self.y_slider.setOrientation(QtCore.Qt.Horizontal)
        self.y_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.y_slider.setTickInterval(10)
        self.y_slider.setObjectName("y_slider")
        self.y_crop = QtWidgets.QLabel(self.centralwidget)
        self.y_crop.setGeometry(QtCore.QRect(90, 460, 101, 16))
        self.y_crop.setObjectName("y_crop")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.x_slider.valueChanged.connect(self.xy_change)
        self.y_slider.valueChanged.connect(self.xy_change)
        self.Open.clicked.connect(self.open_dialog_box)
        self.Save.clicked.connect(self.save_pic)

        self.path = None
        self.faces = None
        self.img = None
        self.x_offset = self.x_slider.value()
        self.y_offset = self.y_slider.value()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Save.setText(_translate("MainWindow", "Save"))
        self.Open.setText(_translate("MainWindow", "Open"))
        self.x_crop.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">X_crop</span></p></body></html>"))
        self.y_crop.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Y_crop</span></p><p><br/></p></body></html>"))

    def numpy_to_qimage(self, image):
        qImg = QtGui.QImage()
        if image.dtype == np.uint8:
            if len(image.shape) == 2:
                channels = 1
                height, width = image.shape
                bytesPerLine = channels * width
                qImg = QtGui.QImage(
                    image.data, width, height, bytesPerLine, QtGui.QImage.Format_Indexed8
                )
                qImg.setColorTable([QtGui.qRgb(i, i, i) for i in range(256)])
            elif len(image.shape) == 3:
                if image.shape[2] == 3:
                    height, width, channels = image.shape
                    bytesPerLine = channels * width
                    qImg = QtGui.QImage(
                        image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888
                    )
                elif image.shape[2] == 4:
                    height, width, channels = image.shape
                    bytesPerLine = channels * width
                    fmt = QtGui.QImage.Format_ARGB32
                    qImg = QtGui.QImage(
                        image.data, width, height, bytesPerLine, fmt
                    )
        return qImg

    def update_display(self):
        bronnify.id_save_her(self.path, "temp_bronn.jpg", self.faces, self.x_offset, self.y_offset)
        self.pic.setPixmap(QtGui.QPixmap("temp_bronn.jpg"))

    def xy_change(self):
        self.x_offset = self.x_slider.value()
        self.y_offset = self.y_slider.value()
        self.update_display()

    def open_dialog_box(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        self.path = filename[0]
        self.faces = bronnify.detect_victims(self.path)
        # self.img = bronnify.spread_bronn(self.path, self.faces, self.x_offset, self.y_offset)
        # self.img = qimage2ndarray.array2qimage(self.img)
        # self.img = self.numpy_to_qimage(self.img)
        # self.pic.setPixmap(QtGui.QPixmap(self.img))

        self.update_display()

    def save_pic(self):
        destination = QtWidgets.QFileDialog.getSaveFileName(directory="untitled.jpg")
        bronnify.id_save_her(self.path, destination[0], self.faces, self.x_offset, self.y_offset)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
