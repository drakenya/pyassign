from django.core.management.base import BaseCommand
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from ..email import emailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        
        emailings = emailing.Email.get_todays_emails()

        plaintext_email = get_template('schedule/emails/reminder_plaintext.txt')
        html_email = get_template('schedule/emails/reminder_html.html')

        for email, listing in emailings.items():
            text_content = plaintext_email.render({'context': listing})
            html_content = html_email.render({'context': listing})

            email = EmailMultiAlternatives(settings.REMINDER_EMAIL_SUBJECT, text_content, settings.REMINDER_EMAIL_FROM, [email])
            email.attach_alternative(html_content, 'text/html')
            email.send()