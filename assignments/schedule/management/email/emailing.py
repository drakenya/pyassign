from django.db import connection
from django.contrib.auth.models import User
import sys

from ...models import Assignment, Account, Emailer, Part

class Email:
    @staticmethod
    def get_todays_emails():
        sql = """
            SELECT {0}.date, first_name, last_name, email, {3}.name, {0}.description
            FROM {0}
                JOIN {1} ON ({1}.id = {0}.account_id)
                JOIN {2} ON ({2}.id = {1}.user_id)
                JOIN {3} ON ({3}.id = {0}.part_id)
                JOIN {4} ON ({4}.account_id = {1}.id)
            WHERE {0}.date = DATE('now', '+' || {4}.days_before || ' day')
            """.format(Assignment._meta.db_table # {0}
                      ,Account._meta.db_table    # {1}
                      ,User._meta.db_table       # {2}
                      ,Part._meta.db_table       # {3}
                      ,Emailer._meta.db_table    # {4}
            )
        cursor = connection.cursor()
        cursor.execute(sql)

        emailings = {}
        for row in cursor.fetchall():
            date = row[0]
            name = "{0} {1}".format(row[1], row[2])
            email = row[3]
            part = row[4]
            part_title = row[5]

            if not email in emailings:
                emailings[email] = {}

            if not date in emailings[email]:
                emailings[email][date] = {'date': date, 'parts': [], 'name': name}

            emailings[email][date]['parts'].append((part, part_title))

        return emailings