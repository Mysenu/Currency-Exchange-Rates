from sqlalchemy import select, func

from .db.create import engine, rate_table


analytic_function = {
    'Maximum': func.max(rate_table.c.value),
    'Minimum': func.min(rate_table.c.value),
    'Average': func.avg(rate_table.c.value),
    'Median': func.median(rate_table.c.value),
    'Range': func.max(rate_table.c.value) - func.min(rate_table.c.value),
    'Middle Range': (func.max(rate_table.c.value) + func.min(rate_table.c.value)) * 0.5
}


def getData(function, code: str, start_date: str, end_date: str, group_mode: int):
    query = (
        select(func.strftime('%Y-%m-%d', rate_table.c.date), function)
            .where(rate_table.c.code == code,
                   start_date <= rate_table.c.date,
                   rate_table.c.date <= end_date)
            .group_by(func.dateid(rate_table.c.date, '%Y-%m-%d', group_mode))
            .order_by(func.date(rate_table.c.date))
    )

    with engine.connect() as conn:
        return conn.execute(query).fetchall()
