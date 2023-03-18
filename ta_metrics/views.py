import multiprocessing as mp
from datetime import datetime
import requests

import numpy as np
import pytz
from dateutil import parser
from django.http import JsonResponse

from slack_oauth.views import auth_check
from .view_helpers.api_call import call_api, get_request
from .view_helpers.daily_helpers import fields_to_pacific_dates, pop_day_container, create_day_container
from .view_helpers.daily_ta_helpers import pop_ta_day_container


@auth_check
def daily_tickets_waits(request):
    """
    Populates container with data on number of tickets and total wait times
    """
    start_date, end_date = get_request(request)

    data = call_api(start_date)
    container = create_day_container(start_date, end_date)

    start_date = start_date.replace(tzinfo=pytz.timezone('US/Pacific'))

    for day in data:
        # Discard entries with null values
        if any(key not in day or not day[key] for key in ['createTime', 'assignedTime', 'completeTime']):
            continue

        try:
            day = fields_to_pacific_dates(day)
        except ValueError:
            continue

        date_idx = (day['createTime'] - start_date).days

        if date_idx < len(container):
            pop_day_container(container, day, date_idx)

    return JsonResponse(container, safe=False)


@auth_check
def get_summary_stats(request):
    """
    Returns summary statistics on wait times for a range of dates
    """
    start_date, end_date = get_request(request)

    data = call_api(start_date)

    date_list = []

    for item in data:
        if 'createTime' in item and item['createTime'] and 'assignedTime' in item and item['assignedTime']:
            assigned = parser.parse(item['assignedTime']).timestamp()
            created = parser.parse(item['createTime']).timestamp()
            if start_date.timestamp() <= assigned <= end_date.timestamp():
                date_list.append(assigned - created)

    date_array = np.array(date_list)

    mean_date = np.mean(date_array) / 60
    median_date = np.median(date_array) / 60
    std_dev = np.std(date_array)/ 60
    avg_time_delta = np.mean(np.abs(date_array - mean_date)) / 60

    summary_data = {'median_date': median_date, 'mean_data':mean_date, 'average_time_delta': avg_time_delta, 'standard_deviation': std_dev}

    return JsonResponse(summary_data, safe=False)

@auth_check
def daily_ta_data(request):
    """
    Populates container with data on number of tickets and total wait times
    """
    start_date, end_date = get_request(request)

    ta_name = request.GET.get('ta').replace('_', ' ')

    data = call_api(start_date)
    container = create_day_container(start_date, end_date)

    start_date = start_date.replace(tzinfo=pytz.timezone('US/Pacific'))

    for day in data:
        # Discard entries with null values
        if any(key not in day or not day[key] for key in ['assignedTo', 'assignedTime', 'completeTime']):
            continue

        if day['assignedTo'] != ta_name:
            continue

        try:
            day = fields_to_pacific_dates(day)
        except ValueError:
            continue

        date_idx = (day['assignedTime'] - start_date).days

        if date_idx < len(container):
            pop_ta_day_container(container, day, date_idx)

    return JsonResponse(container, safe=False)


@auth_check
def ta_summary_stats(request):
    start_date, end_date = get_request(request)

    ta_name = request.GET.get('ta').replace('_', ' ')

    data = call_api(start_date)

    tot_tickets = 0
    tot_time = 0
    unique_students = set()

    for day in data:
        # Discard entries with null values
        if any(key not in day or not day[key] for key in ['assignedTo', 'assignedTime', 'completeTime']):
            continue

        try:
            if day['assignedTo'] != ta_name or datetime.strptime(day['assignedTime'],
                                                                 '%Y-%m-%dT%H:%M:%S.%fZ') > end_date:
                continue

            tot_tickets += 1

            tot_time += (datetime.strptime(day['completeTime'], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.strptime(
                day['assignedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')).total_seconds()

            unique_students.add(day['student'])
        except ValueError:
            continue

    stats = [{'tot_tickets': tot_tickets, 'tot_help_time': tot_time,
              'avg_help_time': tot_time / tot_tickets if tot_tickets != 0 else 0,
              'num_unique_students': len(unique_students)}]

    return JsonResponse(stats, safe=False)


@auth_check
def ta_names(request):
    first_date_on_record = '2022-09-01'

    data = call_api(datetime.strptime(first_date_on_record, '%Y-%m-%d'))

    names = set()

    for ticket in data:
        if any(key not in ticket or not ticket[key] for key in ['assignedTo']):
            continue

        names.add(ticket['assignedTo'])

    return JsonResponse(list(names), safe=False)
