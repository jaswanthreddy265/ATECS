import sys
from PyQt5 import QtWidgets, QtCore
from main_window import Ui_MainWindow  # Import the generated Python file


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Connect the date edit widgets to the validation methods
        self.startDateEdit.dateChanged.connect(self.validate_date_range)
        self.endDateEdit.dateChanged.connect(self.validate_date_range)

        # Initialize the calendar widget with the start and end dates
        self.calendarWidget.clicked.connect(self.update_date_edits)

        # Set initial start and end dates for demonstration purposes
        initial_start_date = QtCore.QDate.currentDate().addDays(-10)
        initial_end_date = QtCore.QDate.currentDate().addDays(10)

        self.startDateEdit.setDate(initial_start_date)
        self.endDateEdit.setDate(initial_end_date)

        self.validate_date_range()

    def validate_date_range(self):
        start_date = self.startDateEdit.date()
        end_date = self.endDateEdit.date()

        if start_date > end_date:
            QtWidgets.QMessageBox.warning(self, 'Invalid Date Range', 'Start date must be before end date.')
            self.startDateEdit.setDate(end_date.addDays(-1))

    def update_date_edits(self, date):
        if self.startDateEdit.hasFocus():
            self.startDateEdit.setDate(date)
        elif self.endDateEdit.hasFocus():
            self.endDateEdit.setDate(date)
        self.validate_date_range()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
