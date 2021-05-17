from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtChart import QChartView, QChart, QValueAxis, QDateTimeAxis, QAbstractSeries


class ChartView(QChartView):
    def __init__(self):
        super(ChartView, self).__init__()

        self._data = {}

        self.setRenderHint(QPainter.Antialiasing)

        self.chart = QChart()
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.setChart(self.chart)

        axis_y = QValueAxis()
        axis_y.setTickCount(10)
        axis_y.setLabelFormat('%f')
        axis_y.setTitleText('Value')
        self.chart.addAxis(axis_y, Qt.AlignLeft)

        axis_x = QDateTimeAxis()
        axis_x.setTickCount(10)
        axis_x.setFormat('dd MMM yyyy')
        axis_x.setTitleText('Date')
        self.chart.addAxis(axis_x, Qt.AlignBottom)

    def clear(self):
        self._data.clear()
        self.chart.removeAllSeries()

    def setTitle(self, text: str):
        self.chart.setTitle(text)

    def removeSeries(self, code: str):
        series = self._data.pop(code)
        series.detachAxis(self.chart.axisX())
        series.detachAxis(self.chart.axisY())
        self.chart.removeSeries(series)

    def updateAxes(self):
        max_x = QDateTime(1099, 1, 1, 1, 1, 0, 0)
        min_x = QDateTime(2099, 1, 1, 1, 1, 0, 0)
        max_y = float('-inf')
        min_y = float('+inf')

        for series in self.chart.series():
            points = series.pointsVector()
            max_x = max(QDateTime.fromMSecsSinceEpoch(points[-1].x()), max_x)
            min_x = min(QDateTime.fromMSecsSinceEpoch(points[0].x()), min_x)
            for point in points:
                max_y = max(point.y(), max_y)
                min_y = min(point.y(), min_y)

        self.chart.axisX().setMax(max_x)
        self.chart.axisX().setMin(min_x)
        self.chart.axisY().setMax(max_y)
        self.chart.axisY().setMin(min_y)

    def addSeries(self, code: str, series: QAbstractSeries):
        self._data[code] = series
        self.chart.addSeries(series)
        series.attachAxis(self.chart.axisX())
        series.attachAxis(self.chart.axisY())
        self.updateAxes()
