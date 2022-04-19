from django.core.management.base import BaseCommand
import datetime
from datetime import datetime
from dateutil.relativedelta import *

from menu.models import MenuDay


class Command(BaseCommand):
    help = 'Fill the calendar'

    def handle(self, *args, **options):
        for i in range(2000):
            new_date = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
            dd = new_date + relativedelta(days=i)
            MenuDay.objects.create(menu_day_date=dd)
        print('Calendar filled')
