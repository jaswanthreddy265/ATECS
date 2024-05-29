from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMdiSubWindow


class MdiSubWindow(QMdiSubWindow):
    sigClosed = pyqtSignal(str)

    def closeEvent(self, event):
        """Get the name of active window about to close
      """
        self.sigClosed.emit(self.windowTitle())
        QMdiSubWindow.closeEvent(self, event)
