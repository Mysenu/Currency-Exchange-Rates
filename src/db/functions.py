from datetime import datetime as dt


class Median:
    def __init__(self):
        self.values = []

    def step(self, value):
        self.values.append(value)

    def finalize(self):
        count = len(self.values)
        self.values.sort()

        if count % 2 == 0:
            return (self.values[count // 2 - 1] + self.values[count // 2]) * 0.5
        else:
            return self.values[count // 2]


class DateUnit:
    Day = 0
    Week = 1
    Month = 2
    Year = 3


def dateID(date: str, frmt: str, unit: int):
    date = dt.strptime(date, frmt)
    if unit == DateUnit.Day:
        delta = date - dt(1990, 1, 1)
        return delta.days
    elif unit == DateUnit.Week:
        delta = date - dt(1990, 1, 1)
        return delta.days // 7
    elif unit == DateUnit.Month:
        return date.strftime('%Y-%m')
    elif unit == DateUnit.Year:
        return date.strftime('%Y')