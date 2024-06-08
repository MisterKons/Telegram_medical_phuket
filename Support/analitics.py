import requests
from .credentials import google_id

GA_TRACKING_ID = google_id


def track_event(category, action, label=None, value=None, user_id=None):
    data = {
        'v': '1',  # API Version
        'tid': GA_TRACKING_ID,  # Tracking ID / Property ID
        'cid': user_id if user_id else '555',  # Anonymous Client ID
        't': 'event',  # Event hit type
        'ec': category,  # Event category
        'ea': action,  # Event action
    }

    if label:
        data['el'] = label

    if value:
        data['ev'] = value

    response = requests.post('https://www.google-analytics.com/collect', data=data)
    return response.status_code


def track_message(user_id):
    return track_event('Bot', 'Message', user_id=user_id)


def track_new_user(user_id):
    return track_event('Bot', 'New User', user_id=user_id)


def track_friends_count(friends_count):
    return track_event('Bot', 'Friends Count', value=friends_count)
