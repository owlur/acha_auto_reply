from datetime import datetime


def datetime2str(origin_datetime):
    now = datetime.now()
    result = '%d월 %d일 %d시' % (origin_datetime.month, origin_datetime.day, origin_datetime.hour)

    if origin_datetime.year > now.year:
        result_year = '%d년 ' % origin_datetime.year
        result = result_year + result

    if origin_datetime.minute != 0:
        result += '%d분' % origin_datetime.minute

    return result