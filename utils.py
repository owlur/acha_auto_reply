from datetime import datetime


def datetime2str(origin_datetime):
    now = datetime.now()
    if origin_datetime.hour > 12:
        hour = '오후 %d시' % (origin_datetime.hour - 12)
    elif origin_datetime.hour == 12:
        hour = '점심 12시'
    elif origin_datetime.hour == 0:
        hour = '밤 12시'
    else:
        hour = '오전 %d시' % origin_datetime
    result = '%d월 %d일 %s' % (origin_datetime.month, origin_datetime.day, hour)

    if origin_datetime.year > now.year:
        result_year = '%d년 ' % origin_datetime.year
        result = result_year + result

    if origin_datetime.minute != 0:
        result += '%d분' % origin_datetime.minute

    return result