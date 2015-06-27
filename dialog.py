#!/usr/bin/env python2
import os, sys
from PIL import Image, ImageFilter, ImageDraw

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "gui"))

# QT
from PyQt4 import QtCore, QtGui

import base
import helpers as h

class BaseDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent, QtCore.Qt.Window)
        self.ui = base.Ui_BaseDialog()
        self.ui.setupUi(self)

        self.connect(self.ui.openFileButton, QtCore.SIGNAL("clicked()"), self._fileSelect)

        self.scene = QtGui.QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.pixmapItem = None;

    def _fileSelect(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, "OpenImage", "src", "Bitmaps (*.bmp)")

        if fileName == "":
            h.warn("No file selected.")
            return

        orgImg = Image.open(str(fileName), mode = 'r').convert()
        h.log("Loaded!")
        self.pixmapItem = QtGui.QPixmap(fileName)
        item = QtGui.QGraphicsPixmapItem(self.pixmapItem)
        self.scene.addItem(item);


        #self.ui.graphicsView

        #QGraphicsScene* scene = new QGraphicsScene();
        #QGraphicsView* view = new QGraphicsView(scene);
        #QGraphicsPixmapItem* item = new QGraphicsPixmapItem(QPixmap::fromImage(image));
        #scene->addItem(item);
        #view->show();




def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Test")

    window = BaseDialog()
    window.show()

    print(sys.exit(app.exec_()))

if __name__ == "__main__":
    main()
