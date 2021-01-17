from datetime import datetime


def date_to_timestamp(date: str):
    dt = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
    return dt.timestamp()