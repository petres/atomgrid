#!/usr/bin/env python2

import os
import sys
from PIL import Image, ImageFilter, ImageDraw

import numpy as np
import matplotlib.image as MImage
import scipy.stats as st
#import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "gui"))

# QT
from PyQt4 import QtCore, QtGui

import base
import helpers as h

import matplotlib.image as MImage


######### SOME AUX FUNCTIONS #########
def gkern(kernlen=21, nsig=3):
    """Returns a 2D Gaussian kernel array."""

    interval = (2*nsig+1.)/(kernlen)
    x = np.linspace(-nsig-interval/2., nsig+interval/2., kernlen+1)
    kern1d = np.diff(st.norm.cdf(x))
    kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
    kernel = kernel_raw/kernel_raw.sum()
    return kernel
#######################################



class BaseDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent, QtCore.Qt.Window)
        self.ui = base.Ui_BaseDialog()
        self.ui.setupUi(self)

        self.connect(self.ui.openFileButton, QtCore.SIGNAL("clicked()"), self._openFile)
        self.connect(self.ui.gaussFilterButton, QtCore.SIGNAL("clicked()"), self._gaussFilter)
        self.connect(self.ui.saveFileButton, QtCore.SIGNAL("clicked()"), self._saveFile)

        #self.connect(self.ui.imageListView, QtCore.SIGNAL("activated()"), self._imageActivated);

        self.ui.imageListView.clicked.connect(self._imageActivated)

        self.ui.gaussFilterButton.setEnabled(False)
        self.ui.saveFileButton.setEnabled(False)

        self.scene = QtGui.QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.pixmapItem = None
        self.selectedItem = None

        self.model = QtGui.QStandardItemModel(self.ui.imageListView)


    def _imageActivated(self, index):
        item = self.model.itemFromIndex(index)
        pixmap = QtGui.QGraphicsPixmapItem(item.pixmap)
        self.scene.addItem(pixmap)
        self.selectedItem = item
        self._checkButtons()


    def _openFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, "OpenImage", "src", "Bitmaps (*.bmp)")

        if fileName == "":
            h.warn("No file selected.")
            return



        h.log("Loaded!")
        #self.pixmapItem = QtGui.QPixmap(fileName)
        #item = QtGui.QGraphicsPixmapItem(self.pixmapItem)
        #self.scene.addItem(item)

        item = QtGui.QStandardItem(os.path.basename(str(fileName)))
        item.imageFileName = str(fileName)
        orgImg = Image.open(str(fileName), mode='r').convert()
        item.image = MImage.pil_to_array(orgImg.convert('L'))
        item.pixmap = QtGui.QPixmap(fileName)

        #item.setCheckable(True)

        self.model.appendRow(item)
        self.ui.imageListView.setModel(self.model)


        self._checkButtons()


    def _saveFile(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, "Choose File",  "dst/image.bmp", "Bitmap (*.bmp)")
        Image.fromarray(self.selectedItem.image).save(str(fileName), "BMP")


    def _gaussFilter(self):
        kernelSize = 7
        imgMatrix = self.selectedItem.image
        size = imgMatrix.shape
        gaussianMatrix = MImage.pil_to_array(Image.new('L', imgMatrix.shape, 0))
        matrix = gkern(kernelSize)
        for i in range(size[1] - (kernelSize - 1)):
            for j in range(size[0] - (kernelSize - 1)):
                iS = i + (kernelSize - 1)/2
                jS = j + (kernelSize - 1)/2
                #print t[i:(i + kernelSize), j:(j + kernelSize)]
                gaussianMatrix[iS, jS] = np.sum(np.multiply(imgMatrix[i:(i + kernelSize), j:(j + kernelSize)], matrix))
                #s[iS, jS] = np.sum(t[i:(i + kernelSize), j:(j + kernelSize)],)/kernelSize**2

        item = QtGui.QStandardItem("new")
        item.imageFileName = None


        item.image = gaussianMatrix
        Image.fromarray(gaussianMatrix).save("bliblop", "BMP")
        item.pixmap = QtGui.QPixmap("bliblop")

        self.model.appendRow(item)
        self.ui.imageListView.setModel(self.model)



    def _checkButtons(self):
        if self.selectedItem is None:
            self.ui.gaussFilterButton.setEnabled(False)
            self.ui.saveFileButton.setEnabled(False)
        else:
            self.ui.gaussFilterButton.setEnabled(True)
            self.ui.saveFileButton.setEnabled(True)


def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Test")

    window = BaseDialog()
    window.show()

    print(sys.exit(app.exec_()))

if __name__ == "__main__":
    main()
