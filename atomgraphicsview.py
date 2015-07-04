#!/usr/bin/env python2

# QT
from PyQt4 import QtCore, QtGui
from math import exp

class AtomGraphicsView(QtGui.QGraphicsView):
    mouseHolding = False
    mousePressCoords = None
    translateCoords = (0, 0)

    def __init__(self, parent):
        super(QtGui.QGraphicsView, self).__init__(parent)
        self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        #self.scaleFactor = 1

    def wheelEvent(self, event):
        scaleFactor = exp(event.delta()*1.0/120/5)
        self.scale(scaleFactor, scaleFactor)
        #print(scaleFactor)

    def mousePressEvent(self, event):
        self.mouseHolding = True
        self.mousePressCoords = (event.x(), event.y())
        return super(AtomGraphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.mouseHolding = False
        return super(AtomGraphicsView, self).mouseReleaseEvent(event)
