import requests


alrim_api_base_url = 'https://api-alimtalk.cloud.toast.com'
api_key =''


def send_message(phone_number, store_name, person_num, date):
    template_num = ''
    target_phone_number = phone_number
