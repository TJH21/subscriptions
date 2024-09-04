from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Drop specific tables from the database."

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS plans_customer;')
            cursor.execute('DROP TABLE IF EXISTS plans_plan;')
            self.stdout.write(self.style.SUCCESS('Successfully dropped tables'))
