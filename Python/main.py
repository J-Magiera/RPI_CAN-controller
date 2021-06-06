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
from PyQt5 import QtWidgets, QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

bus = can.interface.Bus(channel ='can0', bitrate=500000, bustype='socketcan_native')

class Graph(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.grid()
        super(Graph, self).__init__(fig)
        

class CANtxThread(QtCore.QThread):

    def __init__(self):
        super().__init__()
        self.data = []
        self.id = 0
        self._run_flag = True
        self.connectedFlag = False
                
    def tx(self):
        if self.connectedFlag == True:
            msg = can.Message(is_extended_id=False, arbitration_id= self.id, data = self.data)
            bus.send(msg)
            time.sleep(0.01)
    
class CANrxThread(QtCore.QThread):
    messageReceived = QtCore.pyqtSignal(str, str, int)
    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.connectedFlag = False        
        
    def run(self):
        while True:
            self.rx()
    
    def rx(self):      
        if self.connectedFlag == True:            
            time.sleep(0.01)
            received = bus.recv()
            self.messageReceived.emit(str(received.arbitration_id), str(received.dlc),
                                     int.from_bytes(received.data,byteorder='big', signed=False))
      

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("CAN app")
        self.canvas = Graph(self, width=5, height=4, dpi=100)
        n_data = 100
        self.xdata = list(range(n_data))
        self.ydata = list(range(n_data))
        self.plot_ref = None
        self.updatePlot()
        self.filteredID = 0
        toolbar = NavigationToolbar(self.canvas, self)
        
        self.__canRX= CANrxThread()
        self.__canTX= CANtxThread()
        self.__canRX.messageReceived.connect(self.readData)
        
        layout =  QtWidgets.QVBoxLayout()
        VLayout = QVBoxLayout()
        Hlayout = QHBoxLayout()
        Hlayout_2 = QHBoxLayout()
        Hlayout_3 = QHBoxLayout()
        Hlayout_4 = QHBoxLayout()

        self.sendDataLabel = QLabel("Data frame: ")
        self.idLabel = QLabel("ID: ")
        self.idLine = QLineEdit(text ='000', maxLength = 3, enabled = True)
        self.idLine.setFixedSize(40, 20)
        self.DLCLabel = QLabel("DLC: ")
        self.dlcLine = QtWidgets.QSpinBox(maximum = 8, minimum = 0, value = 8)
        self.dlcLine.valueChanged.connect(self.lockData)
        self.D = []
        for x in range(8):
            self.D.append(QLineEdit(text='00', maxLength = 2, enabled=True))
            self.D[x].setFixedSize(30, 20)
        
        self.clearDataB = QtWidgets.QPushButton(text = "Clear data", clicked = self.clearData)
        
        self.filterBox = QtWidgets.QCheckBox(text = "Toggle ID filtration", toggled = self.enableID )
        self.filterID = QtWidgets.QSpinBox(value = 0, minimum = 0, maximum = 2048, enabled =False, valueChanged = self.IDchanged)
        self.filterID.setFixedSize(40, 20)
        
        self.dataLabel = QtWidgets.QLabel("Incoming data")
        self.dataTable = QtWidgets.QTextBrowser()
        self.connectButton = QtWidgets.QPushButton(text="connect", checkable = True, enabled=True, clicked = self.connectCAN)
        
        self.sendDataButton = QtWidgets.QPushButton(text="send", clicked = self.sendData)
        
        Hlayout_3.addWidget(self.filterBox)
        Hlayout_3.addWidget(self.filterID)
        VLayout.addLayout(Hlayout_3)
        Hlayout_4.addWidget(self.dataLabel)
        Hlayout_4.addStretch(0)
        Hlayout_4.addWidget(self.clearDataB)
        VLayout.addLayout(Hlayout_4)
        VLayout.addWidget(self.dataTable)
        Hlayout.addWidget(self.idLabel)
        Hlayout.addWidget(self.idLine)
        Hlayout.addWidget(self.DLCLabel)
        Hlayout.addWidget(self.dlcLine)
        Hlayout.addWidget(self.sendDataLabel)
        for textEdit in self.D:
            Hlayout.addWidget(textEdit)

        Hlayout.addStretch(0)
        Hlayout.addWidget(self.sendDataButton)
        Hlayout.addWidget(self.connectButton)
        Hlayout_2.addWidget(self.canvas)
        Hlayout_2.addLayout(VLayout)
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
    
    def clearData(self):
        self.ydata = list(range(100))
        self.dataTable.clear()
    
    def IDchanged(self):
        self.filteredID = self.filterID.text()
     
    def enableID(self, s):
        self.filterID.setEnabled(s)

    def updatePlot(self):
        if self.plot_ref is None:
            plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'r')

            self.plot_ref = plot_refs[0]
        else:
            self.plot_ref.set_ydata(self.ydata)
        self.canvas.axes.set_ylim([min(self.ydata),max(self.ydata)])
        self.canvas.draw()

    def lockData(self):
        # Locks QLineEdits for smaller DLC packages
        for button in self.D:
            button.setEnabled(False)
        for index, button in (zip(range( self.dlcLine.value(),0, -1), self.D)):
            button.setEnabled(True)
    
    def connectCAN(self):
        if self.connectButton.isChecked():
            try:
                os.system("sudo ip link set can0 up type can bitrate 500000")
                time.sleep(1)
                self.connectButton.setChecked(True)
                self.__canRX.start()
                self.__canTX.start()
                self.__canTX.connectedFlag = True
                self.__canRX.connectedFlag = True
                self.timer.start()
            except:
                print("Error #0001")
        else:
            try:
                self.timer.stop()
                self.__canTX.connectedFlag = False
                self.__canRX.connectedFlag = False
                self.__canRX.stop()
                self.__canTX.stop()
                os.system("sudo ip link set down can0")            

                self.connectButton.setChecked(False)
            except:
                self.timer.start()
                print("Error #0002")
                
    def sendData(self):
        try:
            dat = []
            for index, button in (zip(range( self.dlcLine.value(),0, -1), self.D)):
               dat.append(int(button.text(), 16))
            self.__canTX.id = int(self.idLine.text())
            self.__canTX.data = dat
            self.__canTX.tx()

        except:
            print("Error #0003")
            
    def readData(self, arbID, dlc, intD):
        try:
            
            if (int(arbID) == int(self.filteredID) or not self.filterBox.checkState()):
                self.ydata = self.ydata[1:] + [intD]
                self.dataTable.append("ID: " + str(arbID) + " DLC: " + str(dlc) + " Data: " + str(intD) )  
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
