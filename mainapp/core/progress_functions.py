import json
import time
import datetime
import matplotlib.pyplot as plt
import copy
from django.conf import settings
import base64
import io
from .common_functions import get_all_messages, convert_date_to_ms_time_stamp,\
    decode_to_utf8, get_message_type, convert_ms_ts_to_date

month_dict = {1: 'jan', 2: 'fev', 3: 'mar', 4: 'avr', 5: 'mai', 6: 'jun', 7: 'jul', 8: 'aou', 9: 'sept',
              10: 'oct', 11: 'nov', 12: 'dec'}


def get_progress(name: str, mode='per', span='monthly') -> list:
    messages = get_all_messages()
    messages.reverse()
    start_date = datetime.datetime.fromtimestamp(messages[0]['timestamp_ms']/1000).strftime('%m/%Y')

    progress_list = [[start_date, 0]]
    for message in messages:
        date = datetime.datetime.fromtimestamp(message['timestamp_ms']/1000).strftime('%m/%Y')
        if progress_list[-1][0] != date:
            if mode == 'per':
                progress_list.append([date, 0])
            else:
                progress_list.append([date, progress_list[-1][1]])
        if name == 'all' or decode_to_utf8(message['sender_name']) == name:
            progress_list[-1][1] += 1

    return progress_list

def get_progress_versus(names: list) -> dict:
    messages = get_all_messages()
    messages.reverse()
    start_date = datetime.datetime.fromtimestamp(messages[0]['timestamp_ms']/1000).strftime('%m/%Y')
    progress_dict = {name: [[start_date, 0]] for name in names}

    for message in messages:
        date = datetime.datetime.fromtimestamp(message['timestamp_ms']/1000).strftime('%m/%Y')

        if progress_dict[names[0]][-1][0] != date:
            for progress_list in progress_dict.values():
                progress_list.append([date, progress_list[-1][1]])
        name = decode_to_utf8(message['sender_name'])
        if name in names:
            progress_dict[name][-1][1] += 1

    return progress_dict


def get_image_progress(name, mode='per', graph_type='bar'):
    progress_list = get_progress(name, mode)
    x_axis_list = [i for i in range(len(progress_list))]
    vals = [p[1] for p in progress_list]
    keys = [p[0] for p in progress_list] # list of months
    for i in range(0, len(keys), 2):
        keys[i] = ''
    if graph_type == 'bar':
        plt.bar(x_axis_list, vals, align='center')
    else:
        plt.plot(x_axis_list, vals, '-o')
    plt.xticks(x_axis_list, keys, fontsize=6, rotation=30)
    plt.xlabel('date')
    plt.ylabel('messages sent')
    if mode == 'per':
        plt.title(name + "'s messages sent per month")
    else:
        plt.title(name + "'s total messages sent progression")
    flike = io.BytesIO()
    plt.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    plt.close()
    return b64


def get_image_progress_versus(names):
    progress_dict = get_progress_versus(names)
    for name in names:
        progress_list = progress_dict[name]
        x_axis_list = [i for i in range(len(progress_list))]
        vals = [p[1] for p in progress_list]
        keys = [p[0] for p in progress_list]  # list of months
        for i in range(0, len(keys), 2):
            keys[i] = ''

        plt.plot(x_axis_list, vals, '-o')

    plt.xticks(x_axis_list, keys, fontsize=6, rotation=30)
    plt.xlabel('date')
    plt.ylabel('messages sent')
    plt.legend(tuple(names))
    plt.title('total messages sent versus')
    flike = io.BytesIO()
    plt.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    plt.close()
    return b64

def message_value(message, react='all'):
    if 'reactions' in message.keys():
        count = 0
        for reaction in message['reactions']:
            r = decode_to_utf8(reaction['reaction'])
            if react == 'all' or react == r:
                count += 1
        return count
    return 0

def get_best_messages(react, n=1):
    messages = get_all_messages()
    sorted_messages = sorted(messages, key=lambda msg: message_value(msg, react=react), reverse=True)
    return [get_good_msg_display(sorted_messages[i]) for i in range(n)]


def get_good_msg_display(msg):
    rep = {'sender': decode_to_utf8(msg['sender_name'])}
    if 'content' in msg.keys():
        rep['message'] = decode_to_utf8(msg['content'])
    else:
        rep['message'] = '<UN FICHIER>'
    if 'reactions' in msg.keys():
        count_dict = {}
        for reaction in msg['reactions']:
            r = decode_to_utf8(reaction['reaction'])
            if r in count_dict.keys():
                count_dict[r] += 1
            else:
                count_dict[r] = 1
        rep['reactions'] = count_dict
    tms = msg['timestamp_ms']
    date = convert_ms_ts_to_date(tms)
    rep['date'] = date
    return rep

