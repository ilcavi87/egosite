import os
from shutil import copy
#from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.utils import translation

from egonet.models import Group
from egonet.paths import EGONET

default_path = os.path.join(EGONET, os.pardir, 'reports')

class Command(BaseCommand):
    args = 'groupuuid'
    help = 'Collect all pdf reports in a directory'
    #option_list = BaseCommand.option_list + (
    #    make_option('-p',
    #        '--default_path',
    #        action='store',
    #        dest='lang',
    #        default='/tmp',
    #        help='directory to export the ego graphml files'),
    #    )

    def add_arguments(self, parser):
        parser.add_argument('groupuuid')

    def handle(self, *args, **options):
        #if len(args) == 0:
        #    raise CommandError('You have to specify a group uuid')
        #groupuuid = args[0]
        try:
            groupuuid = options['groupuuid']
            group = Group.objects.get(groupuuid=groupuuid)
        except Group.DoesNotExist:
            raise CommandError('Group "%s" does not exist' % groupuuid)

        if not os.path.exists(default_path):
            os.mkdir(default_path)
        group_path = os.path.join(default_path, "group_" + groupuuid)
        if not os.path.exists(group_path):
            os.mkdir(group_path)
        for ego in group.ego_set.filter(completed=True):
            print (ego)
            pdf = ego.get_pdf_path()
            if not pdf:
                self.stdout.write('Ego %s (%s) does not have a report!' % (ego.name, ego.egouuid))
                continue
            copy(pdf, os.path.join(group_path, 
                    "_".join([ego.name.replace(' ',''), ego.egouuid, '.pdf'])))
