# importing required libraries
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import *
import os
import sys
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background : lightgrey;")
        self.img_name = ""

        self.available_cameras = QCameraInfo.availableCameras()
        # if no camera found
        if not self.available_cameras:
            QMessageBox.warning(self, "Warning", "No Camera found")
            sys.exit()

        # creating a status bar
        self.status = QStatusBar()
        self.status.setStyleSheet("background : white;")
        self.setStatusBar(self.status)

        self.save_path = ""

        # creating a QCameraViewfinder object
        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()
        self.setCentralWidget(self.viewfinder)

        self.select_camera(0)  # Default Camera setting

        # creating a tool bar
        toolbar = QToolBar("Camera Tool Bar")
        self.addToolBar(toolbar)

        # creating a photo action to take photo
        click_action = QAction("Click photo", self)
        click_action.setStatusTip("This will capture picture")
        click_action.setToolTip("Capture picture")
        click_action.triggered.connect(self.click_photo)
        toolbar.addAction(click_action)

        # Creating Open action to the toolbar
        open_action = QAction('Open Photo', self)
        open_action.triggered.connect(self.open_photo)
        toolbar.addAction(open_action)

        # creating action for changing save folder
        change_folder_action = QAction("Change save location", self)
        change_folder_action.setStatusTip("Change folder where picture will be saved saved.")
        change_folder_action.setToolTip("Change save location")
        change_folder_action.triggered.connect(self.change_folder)
        toolbar.addAction(change_folder_action)

        # creating a combo box for selecting camera
        camera_selector = QComboBox()
        camera_selector.setStatusTip("Choose camera to take pictures")
        camera_selector.setToolTip("Select Camera")
        camera_selector.setToolTipDuration(2500)

        # adding items to the combo box
        camera_selector.addItems([camera.description()
                                  for camera in self.available_cameras])

        # adding action to the combo box
        # calling the select camera method
        camera_selector.currentIndexChanged.connect(self.select_camera)

        # adding this to tool bar
        toolbar.addWidget(camera_selector)

        # setting tool bar stylesheet
        toolbar.setStyleSheet("background : white;")

        # setting window title
        self.setWindowTitle("Emirates ID Photo Catcher")
        self.setWindowIcon(QIcon('logo.png'))
        # showing the main window
        self.show()

        # method to select camera

    def select_camera(self, i):

        # getting the selected camera
        self.camera = QCamera(self.available_cameras[i])

        # setting view finder to the camera
        self.camera.setViewfinder(self.viewfinder)

        # setting capture mode to the camera
        self.camera.setCaptureMode(QCamera.CaptureStillImage)

        # if any error occur show the alert
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))

        # start the camera
        self.camera.start()

        # creating a QCameraImageCapture object
        self.capture = QCameraImageCapture(self.camera)

        # showing alert if error occur
        self.capture.error.connect(lambda error_msg, error,
                                          msg: self.alert(msg))

        # when image captured showing message
        self.capture.imageCaptured.connect(lambda d,
                                                  i: self.status.showMessage("Image captured : "
                                                                             + str(self.save_seq)))

        # getting current camera name
        self.current_camera_name = self.available_cameras[i].description()

        # inital save sequence
        self.save_seq = 0

    # method to take photo
    def click_photo(self):
        if self.save_path == "":
            QMessageBox.warning(self, "Warning", "Select a folder")
        # time stamp
        else:
            timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
            img_name = QInputDialog.getText(self, 'Text Input Dialog', 'Enter Pic Name:')[0]
            self.capture.capture(os.path.join(self.save_path, "%s.jpg" % (img_name)))

            self.img_name = '{}/{}.jpg'.format(self.save_path, img_name)

    def open_photo(self):
        print(self.img_name)
        if self.img_name == "":

            QMessageBox.warning(self, "Warning", "No image Found")
        else:
            self.child = img_window(self.img_name)

    # change folder method
    def change_folder(self):
        # open the dialog to select path
        path = QFileDialog.getExistingDirectory(self,
                                                "Picture Location", "")

        # if path is selected
        if path:
            # update the path
            self.save_path = path

            # update the sequence
            self.save_seq = 0

    # method for alerts
    def alert(self, msg):

        # error message
        error = QErrorMessage(self)

        # setting text to the error message
        error.showMessage(msg)


class img_window(QWidget):
    def __init__(self, img_name):
        super().__init__()
        name = img_name
        self.setWindowTitle('Picture')
        self.img_layout = QVBoxLayout()
        self.labe = QLabel()
        self.img = QPixmap(name)
        self.labe.setPixmap(self.img)
        self.labe.resize(self.img.width(), self.img.height())
        self.img_layout.addWidget(self.labe)
        self.setLayout(self.img_layout)
        self.show()


# Driver code
if __name__ == "__main__":
    # create pyqt5 app
    App = QApplication(sys.argv)

    # create the instance of our Window
    window = MainWindow()

    # start the app
    sys.exit(App.exec())