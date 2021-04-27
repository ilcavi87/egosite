import os
from time import sleep

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage

from egonet.models import Group

email_from = 'no-reply@networker.webfactional.com'
email_subject = 'Your Social Netowk Survey PDF report'
email_body = """Dear %s,

Please find attached your personalized PDF report from the Social Network survey that you completed.

Best Regards,

networker.webfactional.com
"""

class Command(BaseCommand):
    args = 'groupuuid'
    help = 'Send all pdf reports vie email'

    def add_arguments(self, parser):
        parser.add_argument('groupuuid')

    def handle(self, *args, **options):
        #if len(args) == 0:
        #    raise CommandError('You have to specify a group uuid')

        groupuuid = options['groupuuid']

        try:
            group = Group.objects.get(groupuuid=groupuuid)
        except Group.DoesNotExist:
            raise CommandError('Group "%s" does not exist' % groupuuid)

        for ego in group.ego_set.filter(completed=True):
            pdf_report = ego.get_pdf_path()

            if not pdf_report:
                self.stdout.write('Ego %s (%s) does not have a report!' % (ego.name, ego.egouuid))
                continue

            email = EmailMessage(
                email_subject,
                email_body % ego.first_name,
                email_from,
                [ego.email],
            )
            email.attach_file(pdf_report)
            email.send()
            sleep(1)
