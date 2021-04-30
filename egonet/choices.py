from django.utils.translation import ugettext as _

GENDER_CHOICES = (
    ('M', _('Male')),
    ('F', _('Female'))
)

#SALARY_CHOICES = (
#    (1, _(u'less than 30,000 euros')),
#    (2, _(u'31,000 -- 50,000 euros')),
#    (3, _(u'51,000 -- 70,000 euros')),
#    (4, _(u'71,000 -- 90,000 euros')),
#    (5, _(u'91,000 -- 110,000 euros')),
#    (6, _(u'111,000 -- 150,000 euros')),
#    (7, _(u'151,000 -- 200,000 euros')),
#    (8, _(u'201,000 -- 300,000 euros')),
#    (9, _(u'301,000 -- 500,000 euros')),
#    (10, _(u'more than 500,000 euros')),
#)

F_AREA_CHOICES = (
    (1, _('Sales')),
    (2, _('Service')),
    (3, _('Manufacturing')),
    (4, _('Engineering/Research')),
    (5, _('Marketing/Distribution')),
    (6, _('Finance')),
    (7, _('Human resources')),
    (8, _('General Management')),
    (9, _('Other')),
    (10, _('Not working')),
)

EDUCATION_CHOICES = (
    (1, _('Primary School')),
    (2, _('High School')),
    (3, _('College or Equivalent')),
    (4, _('Master')),
    (5, _('Doctorate')),
)

CURRENT_JOB_CHOICES = (
    (1, _('Individual Contributor')),
    (2, _('Team Leader')),
    (3, _('Manager')),
    (4, _('Middle Manager')),
    (5, _('Senior Manager')),
    (6, _('CEO/Chairman')),
    (7, _('Self-employed')),
    (8, _('Other')),
)

HELP_CHOICES = (
    (1, _('Not at all')),
    (2, _('Rarely')),
    (3, _('Sometimes')),
    (4, _('Frequently')),
    (5, _('A great deal')),
)

CONTEXT_CHOICES = (
    (1, _('School mate')),
    (2, _('Social/sports club')),
    (3, _('Religious service')),
    (4, _('Voluntary association')),
    (5, _('Political party')),
    (6, _('Business contact')),
    (7, _('Coworker')),
    (8, _('Common friend')),
    (9, _('Other')),
)

WORK_CHOICES = (
    (1, _('Same office/team')),
    (2, _('Same division')),
    (3, _('Different division')),
    (4, _('Different Company')),
    (5, _('Self employed')),
    (6, _('Not working')),
)

RANK_CHOICES = (
    (1, _('Higher')),
    (2, _('Similar')),
    (3, _('Lower')),
    (4, _('Self employed')),
    (5, _('Not working')),
)

FREQUENCY_CHOICES = (
    (1, _('Daily')),
    (2, _('Weekly')),
    (3, _('Monthly')),
    (4, _('Less often')),
)

STRENGTH_CHOICES = (
    (1, _('Very Close')),
    (2, _('Close')),
    (3, _('Neutral')),
    (4, _('Distant')),
)

choices_dict = dict([
    ('helps', HELP_CHOICES),
    ('freq', FREQUENCY_CHOICES),
    ('context', CONTEXT_CHOICES),
    ('strength', STRENGTH_CHOICES),
    ('rank', RANK_CHOICES),
    ('work', WORK_CHOICES),
    ('functional_area', F_AREA_CHOICES),
])

