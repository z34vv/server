import datetime
import random
import string
import hashlib
import uuid
import pycountry
import phonenumbers


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


email = "quanghuyndvc@gmail.com"
email_2 = "deathzerono1@gmail.com"


print(len(generateUserID(email, "VN")))
print(generateUserID(email_2, "VN"))

