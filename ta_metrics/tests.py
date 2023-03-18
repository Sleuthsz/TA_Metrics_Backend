import unittest
import requests
from datetime import datetime, time, timedelta
from django.apps import apps
from django.test import TestCase
from unittest.mock import patch
from ta_metrics.views import call_api
from ta_metrics.apps import TaMetricsConfig
from ta_metrics.view_helpers.daily_helpers import get_hour_str, to_pacific_time, pop_day_container



class TaMetricsConfigTests(TestCase):
    def test_ta_metrics_app(self):
        self.assertEqual(TaMetricsConfig.name, 'ta_metrics')
        self.assertTrue(apps.is_installed('ta_metrics'))


class TimezoneConversionTestCase(TestCase):

    def test_to_pacific_time_returns_datetime_object(self):
        time_str = '2022-03-15T12:00:00.000Z'
        result = to_pacific_time(time_str)
        self.assertIsInstance(result, datetime)


class ContainerTests(TestCase):
    def test_pop_day_container(self):
        container = {
            '2023-02-27': {
                'hours': {
                    '10 AM': {'tickets': 0, 'time': 0},
                }
            }
        }
        day = {
            'assignedTime': datetime(2023, 2, 27, 10, 30),
            'createTime': datetime(2023, 2, 27, 10, 0),
        }
        date_idx = '2023-02-27'
        pop_day_container(container, day, date_idx)

        assert container['2023-02-27']['hours']['10 AM']['tickets'] == 1
        assert container['2023-02-27']['hours']['10 AM']['time'] == 1800


class HourConversionTest(TestCase):
    def test_get_hour_str_less_then_twelve(self):
        time_object_hour = time(hour=10)
        expected = '10 AM'
        actual = get_hour_str(time_object_hour)
        self.assertEqual(actual, expected)

    def test_get_hour_str_at_twelve(self):
        new_hour_input = time(hour=12)
        expected = '12 PM'
        actual = get_hour_str(new_hour_input)
        self.assertEqual(actual, expected)

    def test_get_hour_str_more_then_twelve(self):
        hour_over = time(hour=15)
        expected = '3 PM'
        actual = get_hour_str(hour_over)
        self.assertEqual(actual, expected)

    def test_get_hour_str_returns_string(self):
        time_input = time(hour=3)
        expected = get_hour_str(time_input)
        self.assertIsInstance(expected, str)


    def test_call_api_invalid_date(self):
        # Specify start date in the future
        start_date = datetime.now() + timedelta(days=1)

        # Call function and expect ValueError to be raised
        with self.assertRaises(ValueError):
            call_api(start_date)
