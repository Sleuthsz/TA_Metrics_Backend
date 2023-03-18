from datetime import timedelta


def create_day_container(start_date, end_date):
    """
    Creates empty container for get_tickets_and_wait function
    """
    # Ensures a range that start on a Monday and ends on a Sunday (so evenly sized weeks)
    while start_date.weekday() != 0:
        start_date += timedelta(days=1)

    while end_date.weekday() != 6:
        end_date -= timedelta(days=1)

    delta = end_date - start_date
    # days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    #
    # container = [{'week': (start_date + timedelta(days=i)) - timedelta(days=start_date.weekday()),
    #               'days': {day: {'tickets': 0, 'time': 0} for day in days}}
    #              for i in range(delta.days + 1)]
    container = []

    for i in range(delta.days + 1):
        if (start_date + timedelta(days=i)).weekday() == 0:
            week = {'week': start_date + timedelta(days=i),
                    'days': {'Monday': {'tickets': 0, 'time': 0},
                             'Tuesday': {'tickets': 0, 'time': 0},
                             'Wednesday': {'tickets': 0, 'time': 0},
                             'Thursday': {'tickets': 0, 'time': 0},
                             'Friday': {'tickets': 0, 'time': 0},
                             'Saturday': {'tickets': 0, 'time': 0},
                             'Sunday': {'tickets': 0, 'time': 0},
                             }
                    }
            container.append(week)

    return container
