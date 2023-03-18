from .daily_helpers import get_hour_str


def pop_ta_day_container(container, day, date_idx):
    """
    Populates day container
    """
    help_time = day['completeTime'] - day['assignedTime']
    help_time = int(help_time.total_seconds())

    hour_window = get_hour_str(day['assignedTime'])

    container[date_idx]['hours'][hour_window]['tickets'] += 1
    container[date_idx]['hours'][hour_window]['time'] += help_time
