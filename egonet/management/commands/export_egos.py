import os
#from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.utils import translation

from egonet.models import Group
from egonet.paths import EGONET

default_path = os.path.join(EGONET, os.pardir, 'exports')

class Command(BaseCommand):
    help = 'Exports as .graphml all completed surveys, for all groups, to a directory'
    #option_list = BaseCommand.option_list + (
    #    make_option('-p',
    #        '--default_path',
    #        action='store',
    #        dest='lang',
    #        default='/tmp',
    #        help='directory to export the ego graphml files'),
    #    )

    def handle(self, *args, **options):

        if not os.path.exists(default_path):
            os.mkdir(default_path)

        for g in Group.objects.all():
            group_path = os.path.join(default_path, "group_" + g.groupuuid)
            if not os.path.exists(group_path):
                os.mkdir(group_path)
            g.export_egos_to_dir(group_path)

