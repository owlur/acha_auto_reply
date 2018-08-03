import DB


def check_regist(user_key):
    res = DB.check_regist(user_key)
    if res == 'true':
        return True
    elif res == 'false':
        return False