from .common_functions import get_all_messages, convert_date_to_ms_time_stamp, decode_to_utf8, get_message_type, \
    refactor_dict

REACTS_LIST = ['❤', '😆', '👍', '😮', '😂', '👎', '🤡', '🗿', 'other']  # list of reacts we want to track


def get_personal_stats(name: str, start_date="30/01/2000", end_date="30/01/2023", word='hi') -> dict:
    """get stats for given user"""
    messages = get_all_messages()
    character_count, message_count = 0, 0  # count characters and number of messages used by user
    word_count = 0  # count number of times specified word was used by user

    received_emoji_count_dict = {k: 0 for k in REACTS_LIST}  # keys = emoji, values = number received by subject
    distributed_emoji_count_dict = {k: 0 for k in REACTS_LIST}  # keys = emoji, values = number sent by subject

    received_emoji_name_dict = {}  # keys = names, values = number of reacts sent to subject, from names
    distributed_emoji_name_dict = {}  # keys = names, values = number sent to names, from subject

    for message in messages:
        start_ts = int(convert_date_to_ms_time_stamp(start_date))
        end_ts = int(convert_date_to_ms_time_stamp(end_date))
        if start_ts < message['timestamp_ms'] < end_ts:
            if decode_to_utf8(message['sender_name']) == name or name == 'all':
                if 'content' in message.keys():  # update message, character and word count
                    content = decode_to_utf8(message['content'])
                    message_count += 1
                    character_count += len(content)
                    if word.lower() in content.lower():
                        word_count += 1

                if 'reactions' in message.keys():
                    reactions = message['reactions']
                    for reaction in reactions:
                        r = decode_to_utf8(reaction['reaction'])

                        if r in received_emoji_count_dict.keys():
                            received_emoji_count_dict[r] += 1
                        else:
                            received_emoji_count_dict['other'] += 1

                        actor = decode_to_utf8(reaction['actor'])
                        if actor in received_emoji_name_dict.keys():
                            received_emoji_name_dict[actor] += 1
                        else:
                            received_emoji_name_dict[actor] = 1

            if 'reactions' in message.keys():
                reactions = message['reactions']
                for reaction in reactions:
                    actor = reaction['actor']
                    if decode_to_utf8(actor) == name or name == 'all':
                        r = decode_to_utf8(reaction['reaction'])
                        if r in distributed_emoji_count_dict.keys():
                            distributed_emoji_count_dict[r] += 1
                        else:
                            distributed_emoji_count_dict['other'] += 1

                        sender = decode_to_utf8(message['sender_name'])
                        if sender in distributed_emoji_name_dict.keys():
                            distributed_emoji_name_dict[sender] += 1
                        else:
                            distributed_emoji_name_dict[sender] = 1

    #  sort
    received_emoji_count_dict = {k: v for k, v in
                                 sorted(received_emoji_count_dict.items(), key=lambda item: item[1], reverse=True)}
    distributed_emoji_count_dict = {k: v for k, v in
                                    sorted(distributed_emoji_count_dict.items(), key=lambda item: item[1],
                                           reverse=True)}
    received_emoji_name_dict = {k: v for k, v in
                                sorted(received_emoji_name_dict.items(), key=lambda item: item[1], reverse=True)}
    distributed_emoji_name_dict = {k: v for k, v in
                                   sorted(distributed_emoji_name_dict.items(), key=lambda item: item[1], reverse=True)}
    #  reduce name lengths
    received_emoji_name_dict = refactor_dict(received_emoji_name_dict)
    distributed_emoji_name_dict = refactor_dict(distributed_emoji_name_dict)
    total_received = sum(v for v in received_emoji_count_dict.values())
    total_distributed = sum(v for v in distributed_emoji_count_dict.values())

    stats = {'character_count': character_count, 'message_count': message_count,
             'average_message_length': round(character_count / message_count, 2), 'word_count': word_count,
             'received_emoji_count_dict': received_emoji_count_dict,
             'distributed_emoji_count_dict': distributed_emoji_count_dict,
             'total_received': total_received, 'total_distributed': total_distributed,
             'received_emoji_name_dict': received_emoji_name_dict,
             'distributed_emoji_name_dict': distributed_emoji_name_dict}

    return stats



if __name__ == '__main__':
    pass
