from typing import Optional

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QDateTimeEdit, QPushButton, QSpacerItem,
                             QSizePolicy)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtChart import QLineSeries

from ..statistics import stat_functions, getData
from ..db import dateRange, DateUnit, allCurrencies, currencyNameByCode
from .chart import ChartView

DATE_FORMAT = 'yyyy-MM-dd'
DISPLAY_DATE_FORMAT = 'dd.MMM.yyyy'


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self._currencies = {}

        self.setWindowTitle('Currency exchange rate statistics')

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(4)

        self.chart_view = ChartView()
        main_layout.addWidget(self.chart_view)

        side_layout = QVBoxLayout()
        side_layout.setContentsMargins(0, 0, 0, 0)
        side_layout.setSpacing(4)
        main_layout.addLayout(side_layout)

        self.method_combo = QComboBox()
        self.method_combo.setToolTip('Statistical method')
        side_layout.addWidget(self.method_combo)
        for name, method in stat_functions.items():
            self.method_combo.addItem(name, method)

        self.date_unit_combo = QComboBox()
        side_layout.addWidget(self.date_unit_combo)
        self.date_unit_combo.addItem('per day', DateUnit.Day)
        self.date_unit_combo.addItem('per week', DateUnit.Week)
        self.date_unit_combo.addItem('per month', DateUnit.Month)
        self.date_unit_combo.addItem('per year', DateUnit.Year)

        start_date, end_date = dateRange()

        self.start_date_edit = QDateTimeEdit(QDateTime.fromString(start_date, DATE_FORMAT))
        self.start_date_edit.setToolTip('Start date')
        self.start_date_edit.setDisplayFormat(DISPLAY_DATE_FORMAT)
        self.start_date_edit.setCalendarPopup(True)
        side_layout.addWidget(self.start_date_edit)

        self.end_date_edit = QDateTimeEdit(QDateTime.fromString(end_date, DATE_FORMAT))
        self.end_date_edit.setToolTip('End date')
        self.end_date_edit.setDisplayFormat(DISPLAY_DATE_FORMAT)
        self.end_date_edit.setCalendarPopup(True)
        side_layout.addWidget(self.end_date_edit)

        add_layout = QHBoxLayout()
        add_layout.setContentsMargins(0, 4, 0, 4)
        add_layout.setSpacing(4)
        side_layout.addLayout(add_layout)

        self.currencies_combo = QComboBox()
        self.currencies_combo.setToolTip('Currency to add')
        add_layout.addWidget(self.currencies_combo)
        for code, name in allCurrencies():
            self.currencies_combo.addItem(name, code)

        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self._addCurrency)
        add_layout.addWidget(self.add_button)

        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self._clear)
        side_layout.addWidget(self.clear_button)

        spacer = QSpacerItem(0, 0, QSizePolicy.Ignored, QSizePolicy.Expanding)
        side_layout.addSpacerItem(spacer)

        self.method_combo.currentIndexChanged.connect(self.updateChart)
        self.date_unit_combo.currentIndexChanged.connect(self.updateChart)
        self.start_date_edit.dateChanged.connect(self.updateChart)
        self.end_date_edit.dateChanged.connect(self.updateChart)
        self.updateChart()

    def _clear(self):
        self._currencies.clear()
        self.chart_view.clear()

    def _addCurrency(self, code: Optional[str] = None):
        if not code:
            code = self.currencies_combo.currentData(Qt.UserRole)

        start_date = self.start_date_edit.date().toString(DATE_FORMAT)
        end_date = self.end_date_edit.date().toString(DATE_FORMAT)

        data = getData(self.method_combo.currentData(Qt.UserRole),
                       code,
                       start_date,
                       end_date,
                       self.date_unit_combo.currentData(Qt.UserRole))

        series = QLineSeries()
        series.setName(currencyNameByCode(code))
        for date, value in data:
            series.append(QDateTime.fromString(date, DATE_FORMAT).toMSecsSinceEpoch(), value)
        self.chart_view.addSeries(code, series)
        self._currencies[code] = series

    def _removeCurrency(self, code: Optional[str] = None):
        """Fixme: Currently not used"""
        self.chart_view.removeSeries(code)

    def updateChart(self):
        self.chart_view.clear()
        self.chart_view.setTitle(self.method_combo.currentText() + ' ' + self.date_unit_combo.currentText())
        for code in self._currencies:
            self._addCurrency(code)
