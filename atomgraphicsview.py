#!/usr/bin/env python2

# QT
from PyQt4 import QtCore, QtGui
from math import exp

class AtomGraphicsView(QtGui.QGraphicsView):
    def __init__(self, parent):
        super(QtGui.QGraphicsView, self).__init__(parent)
        #self.scaleFactor = 1

    def wheelEvent(self, event):
        scaleFactor = exp(event.delta()*1.0/120/5)
        self.scale(scaleFactor, scaleFactor)
        #print(scaleFactor)