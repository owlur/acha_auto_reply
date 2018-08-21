import requests


alrim_api_base_url = 'https://api-alimtalk.cloud.toast.com'
app_key ='OrJbsCa3geKuuqv8'
secret = 'Ycdr64tw'

header = {'X-Secret-Key': secret, 'Content-Type': 'application/json;charset=UTF-8'}

plusFriendId = 'ah_cha'


def send_interval_alrim(phone_number, store_name, person_name, person_num, date, token):
    template_code = ''


def send_alrim(template_code, phone_number, template_parameter):
    params = {
        "plusFriendId": plusFriendId,
        "templateCode": template_code,
        "recipientList": [{
            "recipientNo": phone_number,
            "templateParameter": template_parameter
        }]
    }

    res = requests.post(alrim_api_base_url + '/alimtalk/v1.0/appkeys/' + app_key + '/messages', json=params,
                        headers=header)
    return res.json()