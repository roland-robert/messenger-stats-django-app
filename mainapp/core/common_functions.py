import json
import time
import datetime
from django.conf import settings
import copy


def get_all_messages() -> list:
    messages = []  # list of dictionaries
    i = 0
    while True:
        i += 1
        try:
            file_name = str(settings.BASE_DIR) + '/static/' + f'message_{i}.json'
            with open(file_name) as f:
                data = json.load(f)
                messages = messages + data['messages']  # list of dictionnaries
        except:
            break
    return messages


def get_all_names() -> list:
    messages = get_all_messages()
    name_set = set()
    for message in messages:
        name_set.add(decode_to_utf8(message['sender_name']))
    return list(name_set)


def convert_date_to_ms_time_stamp(date: str) -> float:
    """
    date format : "30/12/2020"
    return timestamp in milliseconds
    """
    ts = time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())
    return 1000 * ts


def reduce_name(title: str, n1=3, n2=1):
    """
    Takes string like 'name surname' and slices name by n1 and surname by n2
    For example : "John Doe" becomes "Joh D"
    """
    l = title.split(' ')
    name, surname = l[0], l[1]
    name, surname = name[:n1], surname[:n2]
    return name + ' ' + surname


def refactor_dict(leader_board_dict: dict) -> dict:
    """takes leader board dict and reduces titles"""
    d_copy = copy.deepcopy(leader_board_dict)
    for key in leader_board_dict.keys():
        d_copy[reduce_name(key)] = d_copy.pop(key)
    return d_copy


def convert_ms_ts_to_date(tms: float) -> str:
    return datetime.datetime.fromtimestamp(tms/1000).strftime('%d/%m/%Y')


def decode_to_utf8(s='\u00f0\u009f\u0098\u0086') -> str:
    """converts to utf-8"""
    return s.encode("latin-1").decode("utf-8")


def get_message_type(message) -> list:
    """types are : 'all', 'file', 'text' """
    message_types = ['all']
    if 'content' in message.keys():
        message_types.append('text')
    else:
        message_types.append('file')
    return message_types
