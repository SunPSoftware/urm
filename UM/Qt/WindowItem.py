# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the AGPLv3 or higher.

from PyQt5.QtCore import QObject, QCoreApplication, QEvent, QRectF, QRect, Qt, pyqtSlot, pyqtProperty, QByteArray, pyqtSignal
from PyQt5.QtQuick import QQuickItem, QQuickWindow

class WindowItem(QQuickItem):
    def __init__(self, parent = None):
        super(WindowItem, self).__init__(parent)
        self.__windowItem = None
        self.__bchanged = False
        self.__bfirstshow = True
        self.windowChanged.connect(self.slotWindowChanged)

    windowItemChanged = pyqtSignal()

    @pyqtProperty(QQuickWindow, notify = windowItemChanged)
    def windowItem(self):
        return self.__windowItem

    @windowItem.setter
    def windowItem(self, winitem):
        if self.__windowItem == winitem:
            return
        self.__windowItem = winitem
        self.windowItemChanged.emit()
        self.slotWindowChanged(self.window())

    @pyqtSlot(QQuickWindow)
    def slotWindowChanged(self, winitem):
        if winitem is not None and self.__windowItem is not None:
            self.__windowItem.setParent(winitem)
            self.__windowItem.setFlags(Qt.Widget)

    @pyqtSlot()
    def slotGeometryChanged(self):
        if not self.__bchanged:
            QCoreApplication.postEvent(self, QEvent(QEvent.User))
            self.__bchanged = True

    @pyqtSlot()
    def slotVisibleChanged(self):
        if self.isVisible():
            if self.__bfirstshow:
                QCoreApplication.postEvent(self, QEvent(QEvent.User + 1))
                self.__bfirstshow = False
            else:
                self.__windowItem.show()
                self.setWindowGeometry()
        else:
            self.__windowItem.hide()

    def setWindowGeometry(self):
        pitem = self.parentItem()
        if pitem is not None and self.__windowItem is not None:
            if self.isVisible():
                self.__windowItem.hide()
            rect1 = QRectF(self.x(),self.y(),self.width(),self.height())
            rect2 = pitem.mapRectToScene(rect1)
            self.__windowItem.setGeometry(rect2.toRect())
            if self.isVisible():
                self.__windowItem.show()
        self.__bchanged = False

    def event(self, ev):
        if ev.type() == QEvent.User:
            self.setWindowGeometry()
            return True
        elif ev.type() == QEvent.User + 1:
            if self.isVisible():
                self.__windowItem.show()
            return True
        return super().event(ev)
