# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import subprocess


def is_ideapad_module_loaded():
    try:
        output = subprocess.check_output(
            "lsmod | grep ideapad_laptop", shell=True)
        return "ideapad_laptop" in output.decode()
    except subprocess.CalledProcessError:
        return False


def find_device_path():
    path = "/sys/bus/platform/drivers/ideapad_acpi/"
    try:
        contents = subprocess.check_output(
            f"ls {path}", shell=True).decode().strip().split('\n')
        for item in contents:
            if item.startswith("VPC"):
                return path + item
        return None
    except subprocess.CalledProcessError:
        return None


def get_conservation_mode_status(device_path):
    try:
        with open(device_path + "/conservation_mode", "r") as file:
            return file.read().strip() == "1"
    except IOError:
        return False


def set_conservation_mode_status(device_path, enabled):
    status = "1" if enabled else "0"
    try:
        subprocess.check_output(
            f"echo {status} | sudo tee {device_path}/conservation_mode", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(264, 181)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(10, 40, 92, 23))
        self.checkBox.setObjectName("checkBox")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 211, 31))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(
            self.centralwidget)  # Renamed from saveButton
        self.pushButton.setGeometry(QtCore.QRect(130, 70, 89, 25))
        self.pushButton.setStyleSheet("QPushButton#pushButton {\n"
                                      "    color: Green;\n"
                                      "    background-color: lightgray;\n"
                                      "    font-weight: bold;\n"
                                      "    padding: 5px;\n"
                                      "}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(
            self.centralwidget)  # Renamed from cancelButton
        self.pushButton_2.setGeometry(QtCore.QRect(10, 70, 89, 25))
        self.pushButton_2.setStyleSheet("QPushButton#pushButton_2 {\n"
                                        "    color: red;\n"
                                        "    background-color: lightgray;\n"
                                        "    font-weight: bold;\n"
                                        "    padding: 5px;\n"
                                        "}")
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(10, 100, 251, 31))
        self.textBrowser_2.setObjectName("textBrowser_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 264, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.initializeConservationMode()
        self.pushButton.clicked.connect(self.saveConservationMode)
        self.pushButton_2.clicked.connect(self.cancelApplication)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Enable Conservation Mode</p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Save"))
        self.pushButton_2.setText(_translate("MainWindow", "Cancel"))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                              "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Created with love by @sudipnext</p></body></html>"))

    def initializeConservationMode(self):
        if is_ideapad_module_loaded():
            device_path = find_device_path()
            if device_path:
                self.device_path = device_path  # Save the device path for later use
                conservation_mode_enabled = get_conservation_mode_status(self.device_path)
                self.checkBox.setChecked(conservation_mode_enabled)
            else:
                print("Device path not found.")
        else:
            print("ideapad_laptop module not loaded.")

    def saveConservationMode(self):
        if hasattr(self, 'device_path'):
            enabled = self.checkBox.isChecked()
            success = set_conservation_mode_status(self.device_path, enabled)
            if success:
                print("Conservation mode updated successfully.")
            else:
                print("Failed to update conservation mode.")
        else:
            print("Device path not available.")
    def cancelApplication(self):
        QtCore.QCoreApplication.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
