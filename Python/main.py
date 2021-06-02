from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sys
import os
import can
import time
import struct
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit)
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class Graph(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.grid()
        super(Graphs, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("CAN app")
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.bus = can.interface.Bus(channel='can0', bitrate=500000, bustype='socketcan_native')

        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = list(range(n_data))
        self.plot_ref = None
        self.update_plot()
        self.filteredID = 0
        toolbar = NavigationToolbar(self.canvas, self)

        layout = QtWidgets.QVBoxLayout()
        VLayout = QVBoxLayout()
        HLayout = QHBoxLayout()
        HLayout_2 = QHBoxLayout()
        HLayout_3 = QHBoxLayout()
        HLayout_4 = QHBoxLayout()

        self.sendDataLabel = QLabel("Data frame: ")
        self.idLabel = QLabel("ID: ")

        self.idLine = QLineEdit(text='000', maxLength=3, enabled=True)
        self.idLine.setFixedSize(40, 20)

        self.DLCLabel = QLabel("DLC: ")
        self.dlcLine = QtWidgets.QSpinBox(maximum=8, minimum=0, value=8)
        self.dlcLine.valueChanged.connect(self.lockDataButtons)

        self.D = []
        for x in range(8):
            self.D.append(QLineEdit(text='00', maxLength=2, enabled=True))
            self.D[x].setFixedSize(30, 20)

        self.clearDataB = QtWidgets.QPushButton(text="Clear data", clicked=self.clearData)

        self.filterBox = QtWidgets.QCheckBox(text="Toggle ID filtration", toggled=self.enableID)
        self.filterID = QtWidgets.QSpinBox(value=0, minimum=0, maximum=2048, enabled=False, valueChanged=self.changedID)
        self.filterID.setFixedSize(40, 20)

        self.dataLabel = QtWidgets.QLabel("Incoming data")
        self.dataTable = QtWidgets.QTextBrowser()
        self.connectButton = QtWidgets.QPushButton(text="connect", checkable=True, enabled=True,
                                                   clicked=self.connectCAN)

        self.sendSthButton = QtWidgets.QPushButton(text="send", clicked=self.sendToCAN)

        HLayout_3.addWidget(self.filterBox)
        HLayout_3.addWidget(self.filterID)
        VLayout.addLayout(HLayout_3)
        HLayout_4.addWidget(self.dataLabel)
        HLayout_4.addStretch(0)
        HLayout_4.addWidget(self.clearDataB)
        VLayout.addLayout(Hlayout_4)
        VLayout.addWidget(self.dataTable)
        HLayout.addWidget(self.idLabel)
        HLayout.addWidget(self.idLine)
        HLayout.addWidget(self.DLCLabel)
        HLayout.addWidget(self.dlcLine)
        HLayout.addWidget(self.sendDataLabel)

        for lineEdit in self.D:
            HLayout.addWidget(lineEdit)

        HLayout.addStretch(0)
        HLayout.addWidget(self.sendSthButton)
        HLayout.addWidget(self.connectButton)
        HLayout_2.addWidget(self.canvas)
        HLayout_2.addLayout(VLayout)
        layout.addWidget(toolbar)

        layout.addLayout(Hlayout_2)
        layout.addLayout(Hlayout)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.updatePlot)
        self.timer.timeout.connect(self.readFromCAN)

    def clearData(self):
        self.ydata = list(range(50))
        self.dataTable.clear()

    def changedID(self):
        self.filteredID = self.filterID.text()

    def enableID(self, s):
        self.filterID.setEnabled(s)

    def updatePlot(self):
        if self.plot_ref is None:
            plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'r')

            self.plot_ref = plot_refs[0]
        else:
            self.plot_ref.set_ydata(self.ydata)

        self.canvas.axes.set_ylim([min(self.ydata), max(self.ydata)])
        self.canvas.draw()

    def lockDataButtons(self):
        for button in self.D:
            button.setEnabled(False)
        for index, button in (zip(range(self.dlcLine.value(), 0, -1), self.D)):
            button.setEnabled(True)

    def connectCAN(self, s):
        if s:
            try:
                os.system("sudo ip link set can0 up type can bitrate 500000")
                time.sleep(1)
                self.connectButton.setChecked(True)
                self.timer.start()
            except:
                self.timer.stop()
                self.connectButton.setChecked(False)
                print("Error #0001")
        else:
            try:
                self.timer.stop()
                os.system("sudo /sbin/ip link set down can0")
                self.connectButton.setChecked(False)
            except:
                self.timer.start()
                self.connectButton.setChecked(True)
                print("Error #0002")

    def sendToCAN(self):
        try:
            self.bus.flush()
            dat = []
            for index, button in (zip(range(self.dlcLine.value(), 0, -1), self.D)):
                dat.append(int(button.text(), 16))
            msg = can.Message(is_extended_id=False, arbitration_id=int(self.idLine.text(), 16), data=dat)
            self.bus.send(msg)
        except:
            print("Error #0003")

    def readFromCAN(self):
        try:
            message = self.bus.recv()

            id = message.arbitration_id
            data = int.from_bytes(message.data, byteorder='big', signed=False)
            dlc = message.dlc
            if id == int(self.filteredID) or not self.filterBox.checkState():
                self.ydata = self.ydata[1:] + [data]
                self.dataTable.append("ID: " + str(id) + " DLC: " + str(dlc) + " Data: " + str(data))
            else:
                self.ydata = self.ydata[1:] + [0]
                self.dataTable.append("Message with wrong ID")

        except:
            print("CAN not ready")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Breeze')
    window = MainWindow()
    window.show()
    app.exec_()
