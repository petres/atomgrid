#!/usr/bin/env python2

import os
import sys
from PIL import Image, ImageFilter, ImageDraw

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "gui"))

# QT
from PyQt4 import QtCore, QtGui

import base
import helpers as h

import matplotlib.image as MImage

class BaseDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent, QtCore.Qt.Window)
        self.ui = base.Ui_BaseDialog()
        self.ui.setupUi(self)

        self.connect(self.ui.openFileButton, QtCore.SIGNAL("clicked()"), self._openFile)
        #self.connect(self.ui.gaussFilterButton, QtCore.SIGNAL("clicked()"), self._gaussFilter)
        self.connect(self.ui.saveFileButton, QtCore.SIGNAL("clicked()"), self._saveFile)

        self.connect(self.ui.graphicsView, QtCore.SIGNAL("wheel(QWheelEvent)"), self._wheel);

        self.ui.gaussFilterButton.setEnabled(False)
        self.ui.saveFileButton.setEnabled(False)

        self.scene = QtGui.QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.pixmapItem = None
        self.image = None

    def _wheel(self):
        h.warn("WHEEL")

    def _openFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, "OpenImage", "src", "Bitmaps (*.bmp)")

        if fileName == "":
            h.warn("No file selected.")
            return

        orgImg = Image.open(str(fileName), mode='r').convert()
        self.image = MImage.pil_to_array(orgImg.convert('L'))

        h.log("Loaded!")
        self.pixmapItem = QtGui.QPixmap(fileName)
        item = QtGui.QGraphicsPixmapItem(self.pixmapItem)
        self.scene.addItem(item)

        self._checkButtons()

    def _saveFile(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, "Choose File",  "dst/image.bmp", "Bitmap (*.bmp)")
        Image.fromarray(self.image).save(str(fileName), "BMP")


    def _checkButtons(self):
        if self.image is None:
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
