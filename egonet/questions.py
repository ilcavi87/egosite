from django.utils.translation import ugettext as _

default_questions = [
    dict(
        title = _('About this survey'),
        description = _("<p>This survey should take no more than 20 minutes. We will then aggregate the information that you provide in the questions to analyze it, and summarize them in a personalized report which will be emailed to you after all participants of your group have completed the survey.</p>"),
        nexturl = '/add_ego/',
    ),
    dict(
        title = _('Some information about you'),
        description = _("<p>This question is for gathering information about you. The information you provide is confidential and will be used to compare you with your reference group.</p>"),
        nexturl = '/explain/',
    ),
    dict(
        title = _('Add Contacts'),
        description = _("""<p>The following questions identify the people in your contact network. To ensure confidentiality, you are asked to provide only <b>first names</b> and optionally last name initials for each person. Please use names you will be able to recognize in later questions. <b>If two of your contacts have the same first name and initial, make sure you distinguish between the two by using a different first name or initial for one of them.</b> </p>
<p>Each of the following questions refer to a particular type of relationship between you and your contacts.  To reduce the length of the questionnaire, we limit the number of people you can name in each question, but don't feel compelled to fill in all the names if you have fewer contacts for a given type of relationship. As people often have various kinds of relationships with the same person, you can name the same person in more than one question.</p>"""),
        nexturl = '/add_alters/',
    ),
    dict(
        title = _('Add contacts with whom you discuss important matters'),
        description = _("<p> From time to time, most people discuss important matters regarding their job with other people they trust. If you look back over the last six months, who are the three or four people with whom you discussed matters important to you? These can be people at work, family, friends, or advisors.</p>"),
        field = 'important_professional',
        nexturl = '/add_alters/',
    ),
    dict(
        title = _('Add key contacts for getting things done'),
        description = _("<p>Getting things done often requires the buy-in of various key individuals. Suppose you were moving to a new job and wanted to leave behind the best network advice you could for someone moving into your current job. Who are the three or four people you would name to your replacement as essential sources of buy-in to succeed in your current job? These could be people in your function (or division), in another function or even contacts in other firms</p>"),
        field = 'buyin',
        nexturl = '/add_alters/',
    ),
    dict(
        title = _('Add contacts that helped you in your professional achievements'),
        description = _("<p>Considering all the contacts you have made in your career so far and with whom you are still in contact, who have been the most important to your professional achievements? </p>"),
        field = 'important_career',
        nexturl = '/add_alters/',
    ),
    dict(
        title = _('Add contacts that hinder your work'),
        description = _("<p>At the other extreme, who have been the people who had made it the most difficult to carry out your professional responsibilities in the last year or so? We remind you that your responses are confidential</p>"),
        field = 'hinder_professional',
        nexturl = '/add_alters/',
    ),
    dict(
        title = _('Add contacts with whom you spend free time'),
        description = _("<p>Shifting to a broader view of your network, consider the people from your professional network with whom you spend some free time. Over the last six months, who are three or four people you have been with most often for informal social activities such as going out to lunch, dinner, drinks, films, visiting one another's homes, playing sports, and so on? </p>"),
        field = 'free_time',
        nexturl = '/add_alters/',
    ),
    dict(
        title = _('Add your life partner'),
        description = "",
        field = 'life_partner',
        nexturl = '/add_alters/',
        number = 1,
    ),
    dict(
        title = _('Select or add contacts to whom you directly report'),
        description = "",
        field = 'ego_reports_to',
        nexturl = '/add_alters/',
        number = 1,
    ),
    dict(
        title = _('Select or add contacts that report directly to you'),
        description = "",
        field = 'reports_to_ego',
        nexturl = '/explain/',
        number = 1,
    ),
    dict(
        title = _('Information about your contacts'),
        description = _("<p>In the following questions you will be asked to provide information about each one of the contacts that you identified in the previous questions. If you don't know exactly some of the attributes of some of your contacts, please provide your best guess.</p>"),
        nexturl = '/alters_info/',
    ),
    dict(
        # alters_info view. We only need nexturl here
        nexturl = '/compare_alters/',
    ),
    dict(
        attr = 'strength',
        title = _('Strength of the relations with your contacts'),
        description = _("<p>This question is to assess how close are your contacts to you, using the following convention:</p><ul><li><strong>Very Close</strong>: Strong personal bond.</li><li><strong>Close</strong>: Close but without a strong personal bond.</li><li><strong>Neutral</strong>: You can work OK with each other, but no personal bond.</li><li><strong>Distant</strong>: You'd rather avoid and will seek out only if necessary for get your job done.</li></ul>"),
        field = 'strength',
        nexturl = '/compare_alters/',
    ),
    dict(
        attr = 'helps',
        title = _('Help provided by your contacts'),
        description = _("<p>Compare contacts acording to if he or she provides valuable help or technical advice to get your work done efficiently.</p>"),
        field = 'helps',
        nexturl = '/compare_alters/',
    ),
    dict(
        attr = 'freq',
        title = _('Frequency of interaction with your contacts'),
        description = _("<p>How often do you talk or exchange emails with each contact.</p>"),
        field = 'interaction',
        nexturl = '/compare_alters/',
    ),
    dict(
        attr = 'rank',
        title = _('Rank of your contacts'),
        description = _("<p>Contact's formal rank in the organization he/she works for</p>"),
        field = 'rank',
        nexturl = '/compare_alters/',
    ),
    dict(
        attr = 'context',
        title = _('Where did you first meet your contacts?'),
        description = _("<p>Context in which you first met each contact.</p>"),
        field = 'context',
        nexturl = '/compare_alters/',
    ),
    dict(
        attr = 'work',
        title = _('Where do your contacts work?'),
        description = _("<p>Workplace of each of your contacts.</p>"),
        field = 'work',
        nexturl = '/compare_alters/',
    ),
    dict(
        attr = 'functional_area',
        title = _('Functional area of your contacts'),
        description = "",
        field = 'functional_area',
        nexturl = '/explain/',
    ),
    dict(
        title = _('Identify the relations among your contacts'),
        description = _("<p>In the following questions you will be asked to provide information about the relations among the people in your contact network. For each one of the contacts that you identified in the previous questions, you have to select the other contacts that he or she is related to.</p>"),
        nexturl = '/alters_neighbors/',
    ),
    dict(
        # alters_neighbors view. We only need nexturl here
        nexturl = '/explain/',
    ),
    dict(
        title = _('Describe the relations among your contacts'),
        description = _("<p>In the following questions you will be asked to provide information about the nature of the relations among the people in your contact network that you just described in the previous questions. For each one of the relations that you identified, you have to select the kind of relation that they have. If you are not sure, please provide your best guess.</p>"),
        nexturl = '/relationships_attrs/',
    ),
    dict(
        # relationships_attrs view. We only need nexturl here
        nexturl = '/finished/',
    ),
]
