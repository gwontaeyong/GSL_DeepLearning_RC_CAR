import sys
import numpy as np
import os
import cv2 as cv
import threading

from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QApplication, QLabel,
                             QGroupBox)

from PyQt5.QtGui import (QImage, QPixmap)
from PyQt5.QtCore import pyqtSlot, Qt

'''
class for make drive_window application
'''


class Window_GUI(QWidget):
    def __init__(self, path):
        super().__init__()
        self.is_dir(path)
        self.path = path
        '''
        STREELING_LABLES = Labels for rc_car's steering
        SPEED_LABELS = Labels for rc_car's speed
        image_label = Image_Label for show image from RC_CAR
        ex_steering_index, ex_speed_index  = check index of each steering and speed labels
         
       '''
        self.STREELING_LABLES = []
        self.SPEED_LABELS = []
        self.image_label = None
        self.ex_steering_index = 4
        self.ex_speed_index = 0


        # initialize GUI
        self.initUI()

    '''
    initUI
    
    function : initialize GUI
    '''

    def initUI(self):

        steering_box_titl = "RC_STEERING"  # title for steering_box
        steering_label_num = 9  # the number of steering_range
        speed_box_titl = "RC_SPEED"  # title for speed_box
        speed_label_num = 9  # the number of speed_range

        # make steering, speed h box
        h_steering_box = self.return_h_groupbox(steering_box_titl, steering_label_num, self.STREELING_LABLES)
        h_speed_box = self.return_h_groupbox(speed_box_titl, speed_label_num, self.SPEED_LABELS)

        # set initial center label
        style_sheet = 'QLabel { background-color:green;}'
        self.STREELING_LABLES[4].setStyleSheet(style_sheet)
        self.SPEED_LABELS[0].setStyleSheet(style_sheet)

        # make Image_Label
        self.image_label = QLabel("image_label")

        # positioning
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(h_steering_box)
        vbox.addWidget(h_speed_box)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 600)
        self.setWindowTitle('show up the video and value')
        self.show()

    '''
    funtion : is dir
    if there is no dir make new dir
    '''

    def is_dir(self, path):
        if not os.path.isdir("./"+path+"/"):
            os.mkdir("./"+path+"/")

    '''
    setImage
    
    funtion : repaint the Image Label
    input : QImage from RC_CAR
    '''

    @pyqtSlot(np.ndarray)
    def setImage(self, image):

        qt_image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        p = qt_image.scaled(300, 500, Qt.KeepAspectRatio)
        threading.Thread(target=self.capture_image, args=("test", image)).start()
        self.image_label.setPixmap(QPixmap.fromImage(p))


    def capture_image(self, str_, image):
        cv.cvtColor(image, cv.COLOR_BGR2RGB, image)
        get_filename = str(self.ex_steering_index) + "_" + str(self.ex_speed_index) + "_" + datetime.today().strftime(
            "%H_%M_%S_") + ".jpg"
        filepath = os.path.join(self.path, get_filename)
        cv.imwrite(filepath, image)
    """
    repaint_steering_labels
    funtion : repaint steering label
    input : index = index of steering, color = the color want to paint 
    """

    @pyqtSlot(int, str)
    def repaint_steering_labels(self, index, color="green"):
        if index != self.ex_steering_index:
            self.STREELING_LABLES[self.ex_steering_index].setStyleSheet('QLabel { background-color:white;}')
            self.STREELING_LABLES[index].setStyleSheet('QLabel { background-color:' + color + ';}')
        self.ex_steering_index = index

    '''
    repaint_speed_labels
    function : repaint_speed_labels
    input : index = index of steering, color = the color want to paint  
    '''

    @pyqtSlot(int, str)
    def repaint_speed_labels(self, index, color="green"):
        if index != self.ex_speed_index:
            self.SPEED_LABELS[self.ex_speed_index].setStyleSheet('QLabel { background-color:white;}')
            self.SPEED_LABELS[index].setStyleSheet('QLabel { background-color:' + color + ';}')
        self.ex_speed_index = index

    '''
    return_h_groupbox
    
    function : make groupbox
    input : title = the title , num_label = the number of labels , list_label = Array for save labels object
    output : groupbox
    '''

    def return_h_groupbox(self, title, num_label, list_label):

        h_group_box = QGroupBox(title)
        layout = QHBoxLayout()
        for i in range(1, num_label + 1):
            label = QLabel()
            style_sheet = 'QLabel { background-color:white;}'
            label.setStyleSheet(style_sheet)
            list_label.append(label)
            layout.addWidget(label)

        h_group_box.setLayout(layout)

        return h_group_box


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window_GUI()
    sys.exit(app.exec_())
