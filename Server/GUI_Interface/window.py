import sys

from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout,
                             QApplication, QLabel,
                             QGroupBox)

from PyQt5.QtGui import (QImage, QPixmap)
from PyQt5.QtCore import pyqtSlot


'''
class for make window application
'''
class Window_GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.STREELING_LABLES = []
        self.SPEED_LABELS = []
        self.image_label = None
        self.initUI()
        self.ex_steering_index = 4
        self.ex_speed_index = 0

    '''
    initialize GUI
    
    '''
    def initUI(self):

        steering_box_titl = "RC_STEERING" #title for steering_box
        steering_label_num = 9 # the number of steering_range
        speed_box_titl = "RC_SPEED" #title for speed_box
        speed_label_num = 9 # the number of speed_range

        #make steering, speed box
        h_steering_box = self.return_h_groupbox(steering_box_titl, steering_label_num, self.STREELING_LABLES)
        h_speed_box = self.return_h_groupbox(speed_box_titl, speed_label_num, self.SPEED_LABELS)
        style_sheet = 'QLabel { background-color:green;}'
        self.STREELING_LABLES[4].setStyleSheet(style_sheet)
        self.SPEED_LABELS[0].setStyleSheet(style_sheet)

        #make Image_Label
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
    def repaint_steering_labels(self, index, color = "green"):
        print("index ", index)
        if index != self.ex_steering_index:
            self.STREELING_LABLES[self.ex_steering_index].setStyleSheet('QLabel { background-color:white;}')
            self.STREELING_LABLES[index].setStyleSheet('QLabel { background-color:' + color + ';}')
        self.ex_steering_index = index

    @pyqtSlot(int, str)
    def repaint_speed_labels(self, index, color):
        print("index ", index)
        if index != self.ex_speed_index:
            self.SPEED_LABELS[self.ex_speed_index].setStyleSheet('QLabel { background-color:white;}')
            self.SPEED_LABELS[index].setStyleSheet('QLabel { background-color:' + color + ';}')
        self.ex_speed_index = index

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