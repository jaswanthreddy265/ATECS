"""import sys, os
from PyQt5 import QtCore, QtWidgets, QtPrintSupport

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle('Document Printer')
        self.editor = QtWidgets.QTextEdit(self)
        self.editor.textChanged.connect(self.handleTextChanged)
        self.buttonOpen = QtWidgets.QPushButton('Open', self)
        self.buttonOpen.clicked.connect(self.handleOpen)
        self.buttonPrint = QtWidgets.QPushButton('Print', self)
        self.buttonPrint.clicked.connect(self.handlePrint)
        self.buttonPreview = QtWidgets.QPushButton('Preview', self)
        self.buttonPreview.clicked.connect(self.handlePreview)
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.editor, 0, 0, 1, 3)
        layout.addWidget(self.buttonOpen, 1, 0)
        layout.addWidget(self.buttonPrint, 1, 1)
        layout.addWidget(self.buttonPreview, 1, 2)
        self.handleTextChanged()

    def handleOpen(self):
        path = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open file', '',
            'PDF files (*.pdf)')[0]
        if path:
            file = QtCore.QFile(path)
            if file.open(QtCore.QIODevice.ReadOnly):
                stream = QtCore.QTextStream(file)
                text = stream.readAll()
                info = QtCore.QFileInfo(path)
                if info.completeSuffix() == 'pdf':
                    self.editor.document().setPlainText(text)
                else:
                    self.editor.setPlainText(text)
                file.close()

    def handlePrint(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.editor.document().print_(dialog.printer())

    def handlePreview(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.editor.print_)
        dialog.exec_()

    def handleTextChanged(self):
        enable = not self.editor.document().isEmpty()
        self.buttonPrint.setEnabled(enable)
        self.buttonPreview.setEnabled(enable)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())"""
import os


from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import (QCoreApplication, QEventLoop, QObject, QPointF, Qt,
                       QUrl, pyqtSlot)
from PyQt5.QtGui import QKeySequence, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QProgressBar, QProgressDialog, QShortcut, QMainWindow


class PrintHandler(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.m_page = None
        self.m_inPrintPreview = False

    def setPage(self, page):
        assert not self.m_page
        self.m_page = page
        self.m_page.printRequested.connect(self.printPreview)

    @pyqtSlot()
    def print(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self.m_page.view())
        if dialog.exec_() != QDialog.Accepted:
            return
        self.printDocument(printer)

    @pyqtSlot()
    def printPreview(self):
        if not self.m_page:
            return
        if self.m_inPrintPreview:
            return
        self.m_inPrintPreview = True
        printer = QPrinter()
        preview = QPrintPreviewDialog(printer, self.m_page.view())
        preview.paintRequested.connect(self.printDocument)
        preview.exec()
        self.m_inPrintPreview = False

    @pyqtSlot(QPrinter)
    def printDocument(self, printer):
        loop = QEventLoop()
        result = False

        def printPreview(success):
            nonlocal result
            result = success
            loop.quit()
        progressbar = QProgressDialog(self.m_page.view())
        progressbar.findChild(QProgressBar).setTextVisible(False)
        progressbar.setLabelText("Wait please...")
        progressbar.setRange(0, 0)
        progressbar.show()
        progressbar.canceled.connect(loop.quit)
        self.m_page.print(printer, printPreview)
        loop.exec_()
        progressbar.close()
        if not result:
            painter = QPainter()
            if painter.begin(printer):
                font = painter.font()
                font.setPixelSize(20)
                painter.setFont(font)
                painter.drawText(QPointF(10, 25), "Could not generate print preview.")
                painter.end()


def main():
    import sys

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    app.setApplicationName("Previewer")

    view = QWebEngineView()
    view.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled,True)
    view.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PdfViewerEnabled,True)

    view.load(QUrl.fromLocalFile(os.getcwd()+'\myr.pdf'))
    #view.setUrl(QUrl("https://stackoverflow.com/questions/59438021"))
    view.resize(1024, 750)
    view.show()

    handler = PrintHandler()
    handler.setPage(view.page())

    printPreviewShortCut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_P), view)
    printShortCut = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_P), view)

    printPreviewShortCut.activated.connect(handler.printPreview)
    printShortCut.activated.connect(handler.print)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()