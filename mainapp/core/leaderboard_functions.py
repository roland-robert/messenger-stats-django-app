import json
import time
import datetime
import matplotlib.pyplot as plt
import copy
from django.conf import settings
import base64
import io
from .common_functions import get_all_messages, convert_date_to_ms_time_stamp, decode_to_utf8, get_message_type, refactor_dict

# leaderboard functions


def get_leader_board(start_date="30/01/2000", end_date="30/01/2023") -> dict:
    """
    return dict where
    keys are names and values are how many messages they have sent
    message_type : 'all', 'file', 'text'
    """
    start_ts = int(convert_date_to_ms_time_stamp(start_date))
    end_ts = int(convert_date_to_ms_time_stamp(end_date))

    messages = get_all_messages()
    leader_board_dict = {}
    for message in messages:
        tms = message['timestamp_ms']
        if start_ts < tms < end_ts:
            sender = message['sender_name']
            if sender in leader_board_dict.keys():
                leader_board_dict[sender] += 1
            else:
                leader_board_dict[sender] = 1
    leader_board_dict = {k: v for k, v in sorted(leader_board_dict.items(), key=lambda item: item[1])}  # sort dic
    return leader_board_dict


def get_length_leaderboard(start_date="30/01/2000", end_date="30/01/2023", mode='avg'):
    """name must be in utf8"""
    messages = get_all_messages()
    length_lb_dict = {}  # key is name, value is tuple(somme, count)
    start_ts = int(convert_date_to_ms_time_stamp(start_date))
    end_ts = int(convert_date_to_ms_time_stamp(end_date))
    for message in messages:
        if 'content' in message.keys():
            if start_ts < message['timestamp_ms'] < end_ts:
                content = decode_to_utf8(message['content'])
                name = decode_to_utf8(message['sender_name'])
                if name in length_lb_dict.keys():
                    length_lb_dict[name][0] += len(content)
                    length_lb_dict[name][1] += 1
                else:
                    length_lb_dict[name] = [len(content), 1]
    if mode == 'avg':
        rep = {k: v[0]/v[1] for k, v in sorted(length_lb_dict.items(), key=lambda item: item[1][0]/item[1][1])}
    else:
        rep = {k: v[0] for k, v in sorted(length_lb_dict.items(), key=lambda item: item[1][0])}
    return rep


#  MAIN FUNCTIONS TO GET IMAGES


def get_leader_board_image(start_date="30/01/2000", end_date="30/01/2023",
                           top_best='', top_worst='', graph_type='number'):
    if graph_type == 'number':
        D = get_leader_board(start_date, end_date)  # get leaderboard
        plt.title('messages sent per person between : ' + start_date + ' and ' + end_date)
    elif graph_type == 'avg length':
        D = get_length_leaderboard(start_date, end_date, mode='avg')
        plt.title('avg msg length per person between : ' + start_date + ' and ' + end_date)
    else:
        D = get_length_leaderboard(start_date, end_date, mode='total')
        plt.title('total characters sent per person between : ' + start_date + ' and ' + end_date)

    D = refactor_dict(D)  # reduce names
    D = {k: v for k, v in sorted(D.items(), key=lambda item: item[1])}
    x_axis_list = [i for i in range(len(D))]
    vals = list(D.values())
    keys = list(D.keys())
    if top_best:
        if int(top_best) < len(D):
            x_axis_list = [i for i in range(int(top_best))]
            vals = list(D.values())[len(D)-int(top_best):]
            keys = list(D.keys())[len(D)-int(top_best):]
    elif top_worst:
        if int(top_worst) < len(D):
            x_axis_list = [i for i in range(int(top_worst))]
            vals = list(D.values())[:int(top_worst)]
            keys = list(D.keys())[:int(top_worst)]
    plt.bar(x_axis_list, vals, align='center')
    plt.xticks(x_axis_list, keys, fontsize=6)
    plt.xlabel('name')
    plt.ylabel('messages sent')
    flike = io.BytesIO()
    plt.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    plt.close()
    return b64


if __name__ == '__main__':
    d = get_leader_board()
    print(d.keys())
