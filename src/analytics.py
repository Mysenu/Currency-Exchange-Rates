from sqlalchemy import select, func

from .db.create import engine, value_currencies_table


analytic_function = {
    'Maximum': func.max(value_currencies_table.c.value),
    'Minimum': func.min(value_currencies_table.c.value),
    'Average': func.avg(value_currencies_table.c.value),
    'Median': func.median(value_currencies_table.c.value),
    'Range': func.max(value_currencies_table.c.value) - func.min(value_currencies_table.c.value),
    'Middle Range': (func.max(value_currencies_table.c.value) + func.min(value_currencies_table.c.value)) * 0.5
}


def getData(function, code: str, start_date: str, end_date: str, group_mode: int):
    query = (
        select(func.strftime('%Y-%m-%d', value_currencies_table.c.date), function)
            .where(value_currencies_table.c.code == code,
                   start_date <= value_currencies_table.c.date,
                   value_currencies_table.c.date <= end_date)
            .group_by(func.dateid(value_currencies_table.c.date, '%Y-%m-%d', group_mode))
            .order_by(func.date(value_currencies_table.c.date))
    )

    with engine.connect() as conn:
        return conn.execute(query).fetchall()
