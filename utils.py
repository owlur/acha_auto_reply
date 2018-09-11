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


def generate_button(reserv_list):
    button_list = []
    pre_duplicate_num = 1
    store_name = ''
    date = reserv_list[-1]['reservTime']
    for reserv in reserv_list:
        if date.year == reserv['reservTime'].year and date.month == reserv['reservTime'].month \
                and date.day == reserv['reservTime'].day and store_name == reserv['storeName']:
            pre_duplicate_num += 1
            button_name = '%d월 %d일 %s[%d]' % (date.month, date.day, store_name, pre_duplicate_num)
        else:
            date = reserv['reservTime']
            store_name = reserv['storeName']
            pre_duplicate_num = 1

            button_name = '%d월 %d일 %s' % (date.month, date.day, store_name)

        button_list.append(button_name)
        reserv['button_name'] = button_name

    return button_list