import sys

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QApplication, QLabel,
                             QGroupBox)

from PyQt5.QtGui import (QImage, QPixmap)
from PyQt5.QtCore import pyqtSlot

'''
class for make drive_predict application

'''


class Window_GUI(QWidget):

    def __init__(self):
        super().__init__()

        '''
        STREELING_LABLES = Labels for rc_car's steering
        SPEED_LABELS = Labels for rc_car's speed
        PREDICT_STREELING_LABLES = Labels for Predicted steering
        PREDICT_SPEED_LABLES = Labels for Predicted speed
        
        image_label = Image_Label for show image from RC_CAR
        ex_steering_index, ex_speed_index  = check index of each steering and speed labels

        '''
        self.STREELING_LABLES = []
        self.SPEED_LABELS = []
        self.PREDICT_STREELING_LABLES = []
        self.PREDICT_SPEED_LABLES = []

        self.ex_rc_steering_index = 4
        self.ex_rc_speed_index = 0
        self.ex_predict_steering_index = 4
        self.ex_predict_speed_index = 0

        self.image_label = None

        self.initUI()

    '''
    initUI
    function : initialize GUI
    '''

    def initUI(self):

        h_steering_box = QGroupBox("STEERING_VALUE")
        steering_layout = QVBoxLayout()

        steering_box_titl = "RC_CAR"  # title for steering_box
        predict_steering_box_titl = "PREDICTED"  # title for predict steering_box
        steering_label_num = 9  # the number of predict steering_range

        # make steering, speed box
        rc_steering_box = self.return_h_groupbox(steering_box_titl, steering_label_num, self.STREELING_LABLES)
        predict_steering_box = self.return_h_groupbox(predict_steering_box_titl, steering_label_num,
                                                        self.PREDICT_STREELING_LABLES)
        steering_layout.addWidget(rc_steering_box)
        steering_layout.addWidget(predict_steering_box)

        h_steering_box.setLayout(steering_layout)


        h_speed_box = QGroupBox("SPEED_VALUE")
        speed_layout = QVBoxLayout()

        speed_box_titl = "RC_CAR"  # title for speed_box
        predict_speed_box_titl = "PREDICT"  # title for steering_box
        speed_label_num = 9  # the number of speed_range

        rc_speed_box = self.return_h_groupbox(speed_box_titl, speed_label_num, self.SPEED_LABELS)
        predict_speed_box = self.return_h_groupbox(predict_speed_box_titl, speed_label_num, self.PREDICT_SPEED_LABLES)

        speed_layout.addWidget(rc_speed_box)
        speed_layout.addWidget(predict_speed_box)

        h_speed_box.setLayout(speed_layout)


        style_sheet = 'QLabel { background-color:green;}'

        self.STREELING_LABLES[4].setStyleSheet(style_sheet)
        self.SPEED_LABELS[0].setStyleSheet(style_sheet)
        self.PREDICT_STREELING_LABLES[4].setStyleSheet(style_sheet)
        self.PREDICT_SPEED_LABLES[0].setStyleSheet(style_sheet)

        # make Image_Label
        self.image_label = QLabel("image_label")

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(h_steering_box)
        vbox.addWidget(h_speed_box)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 600)
        self.setWindowTitle('show up the video and value')
        self.show()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.image_label.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(int, str)
    def repaint_rc_steering_labels(self, index, color="green"):

        #print("index ", index)
        if index != self.ex_rc_steering_index:
            self.STREELING_LABLES[self.ex_rc_steering_index].setStyleSheet('QLabel { background-color:white;}')
            self.STREELING_LABLES[index].setStyleSheet('QLabel { background-color:' + color + ';}')
        self.ex_rc_steering_index = index

    @pyqtSlot(int, str)
    def repaint_rc_speed_labels(self, index, color="green"):
        #print("index ", index)
        if index != self.ex_rc_speed_index:
            self.SPEED_LABELS[self.ex_rc_speed_index].setStyleSheet('QLabel { background-color:white;}')
            self.SPEED_LABELS[index].setStyleSheet('QLabel { background-color:' + color + ';}')
        self.ex_rc_speed_index = index

    @pyqtSlot(int, str)
    def repaint_predict_steering_labels(self, index, color="green"):
        print("index ", index)
        if index != self.ex_predict_steering_index:
            self.PREDICT_STREELING_LABLES[self.ex_predict_steering_index].setStyleSheet('QLabel { background-color:white;}')
            self.PREDICT_STREELING_LABLES[index].setStyleSheet('QLabel { background-color:' + color + ';}')
        self.ex_predict_steering_index = index

    @pyqtSlot(int, str)
    def repaint_predict_speed_labels(self, index, color="green"):
        #print("index_predict ", index)
        if index != self.ex_predict_speed_index_index:
            self.PREDICT_SPEED_LABLES[self.ex_predict_speed_index_index].setStyleSheet('QLabel { background-color:white;}')
            self.PREDICT_SPEED_LABLES[index].setStyleSheet('QLabel { background-color:' + color + ';}')
        self.ex_predict_speed_index_index = index

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
