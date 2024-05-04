import datetime
import random
import hashlib
import string
import pycountry
import phonenumbers
import uuid
from django.utils import timezone


def nowDateTime():
    nowTime = str(datetime.datetime.now())
    nowTimeList = []
    for c in nowTime:
        if (c != '-') and (c != ' ') and (c != ':') and (c != '.'):
            nowTimeList.append(c)
    return ''.join(nowTimeList[:16])


def nowDate():
    nowTime = str(datetime.datetime.now())
    nowTimeList = []
    for c in nowTime:
        if (c != '-') and (c != ' ') and (c != ':') and (c != '.'):
            nowTimeList.append(c)
    return ''.join(nowTimeList[2:8])


def generateUserID(email, country_code):
    this_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, email)).split('-')[1:5]
    this_uuid = '-'.join(this_uuid)
    user_id = country_code + nowDate() + '-' + this_uuid
    return user_id


def calculate_age(date_of_birth):
    # Get current date
    today = datetime.date.today()
    dob = date_of_birth
    if dob:
        age = today.year - dob.year
        # Checks if the current date is less than the birth_date in the year
        if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
            age -= 1
        return age
    else:
        return None


def getCountryCode():
    countries = list(pycountry.countries)
    country_code_list = []

    # Duyệt qua danh sách quốc gia và lấy thông tin về mã số điện thoại và tên
    for country in countries:
        country_alpha2 = country.alpha_2
        country_name = country.name

        # Lấy thông tin về mã số điện thoại từ thư viện phonenumbers
        try:
            country_phone_info = phonenumbers.region_code_for_country_code(
                phonenumbers.country_code_for_region(country_alpha2))
            country_phone_code = '+' + str(phonenumbers.country_code_for_region(country_alpha2))
        except phonenumbers.NumberParseException:
            country_phone_info = None
            country_phone_code = None

        country_code_list.append((country_phone_code, country_alpha2))
    return country_code_list


def checkChatPermission(user, this_post):
    if user.is_manager or user.is_superuser:
        return True
    elif this_post.chat_mode == 0:
        return True
    elif (this_post.chat_mode == 1) and (user.user_id in this_post.author.followers):
        return True
    elif (this_post.chat_mode == 2) and (user.user_id in this_post.author.fans):
        return True
    elif (this_post.chat_mode == 3) and (user.user_id in this_post.author.friends):
        return True
    return False


def formatDatetime(created_at):
    now_datetime = timezone.now()
    created_time = now_datetime - created_at

    if created_time.days >= 365:
        return f"{created_time.days // 365} years ago"
    elif created_time.days >= 30:
        return f"{created_time.days // 30} months ago"
    elif created_time.days >= 1:
        return f"{created_time.days} days ago"
    elif created_time.seconds >= 3600:
        return f"{created_time.seconds // 3600} hours ago"
    elif created_time.seconds >= 60:
        return f"{created_time.seconds // 60} minutes ago"
    else:
        return 'few seconds ago'

