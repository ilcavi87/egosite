from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.utils import translation

from egonet.models import Group

class Command(BaseCommand):
    args = 'groupuuid'
    help = 'Builds reports for a specified group'
    #option_list = BaseCommand.option_list + (
    #    make_option('-l',
    #        '--language',
    #        action='store',
    #        dest='lang',
    #        default='en',
    #        help='Language code for translating the reports'),
    #    )
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('groupuuid')

    def handle(self, *args, **options):

        #if len(args) == 0:
        #    raise CommandError('You have to specify a group uuid')

        groupuuid = options['groupuuid']
        
        print ("questo e largs")
        print (groupuuid)

        try:
            group = Group.objects.get(groupuuid=groupuuid)
        except Group.DoesNotExist:
            raise CommandError('Group "%s" does not exist' % groupuuid)

        #if options['lang'] != 'en':
        #    translation.activate(options['lang'])
        #translation.activate('es-es')
        from django.conf import settings
        translation.activate(settings.LANGUAGE_CODE)

        group.build_reports()

        translation.deactivate()

        #self.stdout.write('Successfully build reports for Group "%s"' % groupuuid)
        #self.stdout.write('Trying to use language: %s' % options['lang'])
