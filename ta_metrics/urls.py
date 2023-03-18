from django.urls import path
from .views import daily_tickets_waits, get_summary_stats, daily_ta_data, ta_summary_stats, ta_names

urlpatterns = [
    path('ticket_wait', daily_tickets_waits, name='daily_tickets_waits'),
    path('summary_stats', get_summary_stats, name='get_summary_stats'),
    path('ta_dailies', daily_ta_data, name='daily_ta_data'),
    path('ta_summary', ta_summary_stats, name='ta_summary_stats'),
    path('ta_names', ta_names, name='ta_names'),
]
