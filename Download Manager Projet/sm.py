from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QFileDialog
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
import sys
import os


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 350, 350)
        self.setWindowTitle("IDM simulator")
        self.initUI()

    def initUI(self):
        #progress bar
        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setGeometry(30, 250, 250, 30)

        #Downlowd button
        self.b1 = QtWidgets.QPushButton("Downlowd", self)
        self.b1.move(190, 300)
        self.b1.clicked.connect(self.download)

        #finish button
        self.b2 = QtWidgets.QPushButton("Finished", self)
        self.b2.move(85, 300)
        self.b2.clicked.connect(QCoreApplication.instance().quit)
        self.b2.clicked.connect(self.hide)
        self.b2.setEnabled(False)

        #Open file button
        self.b3 = QtWidgets.QPushButton("select file", self)
        self.b3.move(190, 50)
        self.b3.clicked.connect(self.openFile)

        #Path text box Label
        self.lbl=QtWidgets.QLabel("Path :", self)
        self.lbl.geometry()
        self.lbl.move(0, 10)

        #Path text box
        self.textbox = QLineEdit(self)
        self.textbox.move(40, 10)
        self.textbox.resize(250, 30)

        # Path text box2 Label2
        self.lbl2 = QtWidgets.QLabel("Downlowd as :", self)
        self.lbl2.geometry()
        self.lbl2.move(0, 85)

        # Path text box2
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(98, 85)
        self.textbox2.resize(150, 30)

        # Open folder button
        self.b4 = QtWidgets.QPushButton("selct folder", self)
        self.b4.move(190, 160)
        self.b4.clicked.connect(self.openFolder)

        #Path text box3 Label3
        self.lbl3=QtWidgets.QLabel("Download Path:", self)
        self.lbl3.adjustSize()
        self.lbl3.geometry()
        self.lbl3.move(0, 130)


        #Path text box 3
        self.textbox3 = QLineEdit(self)
        self.textbox3.move(120, 125)
        self.textbox3.resize(200, 30)

        #Path text box4 Label4
        self.lbl4=QtWidgets.QLabel("Nbr of processor:", self)
        self.lbl4.adjustSize()
        self.lbl4.geometry()
        self.lbl4.move(0, 200)


        #Path text box 4
        self.textbox4 = QLineEdit(self)
        self.textbox4.move(120, 195)
        self.textbox4.resize(100, 30)


    def openFolder(self):
        destDir = QFileDialog.getExistingDirectory()
        print(destDir)
        self.textbox3.setText(destDir)

    def download(self):
        IDMsim()

    def openFile(self):
        filename = QFileDialog.getOpenFileName()
        self.textbox.setText(filename[0])
        print(self.textbox.text())



#def IDMsim(path, destination, PNbr):
def IDMsim():
    index = 0
    #PNbr = 100
    PNbr = int(win.textbox4.text())
    #Path = 'exemple.txt'
    Path = win.textbox.text()
    if not os.path.exists(Path):
        print(Path + 'n existe pas')
    elif not os.path.isfile(Path):
        print(Path + 'n est pas un fishier')
    else:
        f = open(Path, 'r')
        size = os.path.getsize(Path)
        child_size = size // PNbr
        if child_size < size / PNbr:
            child_size = child_size +1
        for i in range(PNbr):
            rp, wp = os.pipe()
            rf, wf = os.pipe()
            rf2, wf2 = os.pipe()
            pid_child = os.fork()
            if pid_child == 0:
                os.close(wp)
                os.close(rf)
                os.close(rf2)
                fr = os.fdopen(rp, 'r')
                index = fr.read()
                f.seek((int(index)*child_size))
                fr.close()
                fw = os.fdopen(wf, 'w')
                fw.write(f.read(child_size))
                fw2 = os.fdopen(wf2, 'w')
                fw2.write(str(i))
                fw2.close()
                sys.exit()
            elif pid_child > 0: #pere
                if index==0:
                    #do this once
                    print("do this once")
                os.close(rp)
                os.close(wf)
                os.close(wf2)
                fw = os.fdopen(wp, 'w')
                fw.write(str(index))
                fw.close()
                index = index + 1
                #os.wait()
                fr2 = os.fdopen(rf2, 'r')
                val = fr2.read()
                fr2.close()
                if str(i) == val:
                    #fTel = open('telecharger.txt', 'a')
                    fTel = open(win.textbox3.text()+"/"+win.textbox2.text(), 'a')
                    fr = os.fdopen(rf, 'r')
                    fTel.write(fr.read())
                    fr.close()
                    fTel.close()
                    win.progress.setValue(win.progress.value()+100/PNbr)
                    if win.progress.value() == 99:
                        win.progress.setValue(100)
                        win.b2.setEnabled(True)
        f.close()


app = QApplication(sys.argv)
win = MyWindow()
win.show()
sys.exit(app.exec_())





