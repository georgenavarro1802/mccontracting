import json
import random
import unicodedata
from datetime import datetime
from decimal import Decimal

from django.forms import model_to_dict
from django.http import HttpResponse


def model_to_dict_safe(m, exclude=None):
    if not exclude:
        exclude = []
    d = model_to_dict(m, exclude=exclude)
    for x, y in d.items():
        if type(y) == Decimal:
            d[x] = float(y)
    return d


def dict_safe(d):
    for x, y in d.items():
        if type(y) == Decimal:
            d[x] = float(y)
    return d


def ip_client_address(request):
    try:
        client_address = request.META['HTTP_X_FORWARDED_FOR']
    except Exception:
        client_address = request.META['REMOTE_ADDR']

    return client_address


def generate_file_name(name, original):
    ext = ""
    if original.find(".") > 0:
        ext = original[original.rfind("."):]
    date = datetime.now().date()
    time = datetime.now().time()
    return name + date.year.__str__() + date.month.__str__() + date.day.__str__() + \
           time.hour.__str__() + time.minute.__str__() + time.second.__str__() + ext


def convert_date(s):
    try:
        return datetime(int(s[-4:]), int(s[3:5]), int(s[:2]))
    except Exception:
        return datetime.now()


def convert_datepicker_to_datetime(s):
    """
    datepicker returns a value in this format: '11/14/2018 10:30 PM'
    :param s: datepicker string
    :return:
    """
    try:
        datepicker_obj = s.split(" ")
        date_obj = datepicker_obj[0]
        time_obj = datepicker_obj[1].split(":")
        hh = int(time_obj[0]) if datepicker_obj[2] == "AM" else int(time_obj[0]) + 12
        mm = int(time_obj[1])
        return datetime(int(date_obj[-4:]), int(date_obj[:2]), int(date_obj[3:5]), hh, mm)
    except Exception as ex:
        return datetime.now()


def remove_accents(string):
    return''.join((c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'))


def bad_json(message=None, error=None):
    data = {'result': 'bad'}
    if message:
        data.update({'message': message})
    if error:
        if error == 0:
            data.update({"message": "Bad Request"})
        elif error == 1:
            data.update({"message": "Error saving data"})
        elif error == 2:
            data.update({"message": "Error editing data"})
        elif error == 3:
            data.update({"message": "Error deleting data"})
        elif error == 4:
            data.update({"message": "Permission Denied"})
        elif error == 5:
            data.update({"message": "Error generating info"})
        else:
            data.update({"message": "System Error"})
    return HttpResponse(json.dumps(data), content_type="application/json")


def ok_json(data=None):
    if data:
        if 'result' not in data.keys():
            data.update({"result": "ok"})
    else:
        data = {"result": "ok"}
    return HttpResponse(json.dumps(data), content_type="application/json")


def generate_password():
    passw = ''
    for i in range(4):
        passw += random.choice('0123456789')
    return passw

