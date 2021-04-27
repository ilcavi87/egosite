#-*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

from egonet.choices import (GENDER_CHOICES, F_AREA_CHOICES,
    EDUCATION_CHOICES, CURRENT_JOB_CHOICES, WORK_CHOICES,
    RANK_CHOICES, FREQUENCY_CHOICES, STRENGTH_CHOICES,
    HELP_CHOICES, CONTEXT_CHOICES)

titles = dict(
    network = _(u'Your Social Network'),
    edge_attrs = _(u'Your Relations'),
    node_attrs = _(u'Your Contacts'),
    functional_area = _(u'Functional Area of your contacts (n=%d)'),
    work = _(u'Work place of your contacts (n=%d)'),
    rank = _(u'Rank of your contacts (n=%d)'),
    gender = _(u'Gender of your contacts (n=%d)'),
    age = _(u'Age ranges of your contacts (n=%d)'),
    strength = _(u'How close are you with your contacts? (n=%d)'),
    frequency = _(u'How often do you comunicate? (n=%d)'),
    helps = _(u'How helpful are your contacts (n=%d)'),
    context = _(u'Context where you met your contacts (n=%d)'),
)

choices = dict(
    functional_area = dict(F_AREA_CHOICES),
    work = dict(WORK_CHOICES),
    rank = dict(RANK_CHOICES),
    gender = dict(GENDER_CHOICES),
    strength = dict(STRENGTH_CHOICES),
    frequency = dict(FREQUENCY_CHOICES),
    helps = dict(HELP_CHOICES),
    context = dict(CONTEXT_CHOICES),
)

sections = dict(
    network = _(u"One picture is worth a thousand words, and you might get a better sense for where you are in the company if you try to position yourself in its social graph. Looking at the connections among people that you are directly connected with can provide useful insight. For instance, you might realize you happen to work as the link between otherwise disconnected others, thus being able to bridge the gap among different groups, receiving knowledge and information from all of them and controlling to some extent the information flow among them."),
    edge_attrs = _(u"The quality of the relationships between you and your contacts is a good proxy of their willingness to help, and their diversity affects the extent of the resources and information they can provide. The disposition to help and the breadth of that help may be also shaped by the structure of your network."),
    node_attrs = _(u"The diversity of the attributes of the people that forms your personal social network is a source of different perspectives that can allow you to find innovative solutions to the problems that you face at work. However, it might also increase coordination costs and thus hinder action and decision making."),
    intro = _(u"Thinking about your social network might help you go beyond a simplistic view of what your contacts are (who do you know?) and help you think about how the people in your company are connected to each other (your indirect contacts). The patterns of relations among people in your company, and your concrete position in those patterns, might allow you to access and procure valuable intangible assets, such as good advice, technical knowledge, emotional support, etc."),
    intro_short = _(u"Thinking about your social network might help you go beyond a simplistic view of what your contacts are (who do you know?) and help you think about how the people in your company are connected to each other (your indirect contacts)."),
    example_intro = _(u"If you complte the survey, you will have acces to a web report, just like this example one, along with a detailed pdf report with comparations with your reference group. The report is organized in three parts. First, we analyze your network in terms of the number and the diversity of your contacts. Second, we analyze your network in terms of the kind and the strength of the relationships between you and your contacts. Third, we analyze the structure of your network, focusing on the patterns of relations among your contacts."),
    example_intro_short = _(u"If you complete the survey, you will gain access to a web report similar to the following one. Your full personalized report, with comparison with other program participants, will be emailed to you in PDF the day after the completion date of the survey for your group."),
    start_intro = _(u"The goal of this survey is to help you reflect on your social network, in order to better understand its composition and structure. The structure of your network can help you do your job better and make you more effective at work. To learn about this structure, we will ask you questions on your professional contacts, their characteristics, and their relationships."),
    intro_survey = _(u"This survey should take no more than 20 minutes. We will then aggregate this information to analyze it, and summarize them in a personalized report which will be emailed to you after all participants have completed the survey. A shorter sample report will be available on the website as soon as you complete the survey. "),
    intro_latex = (
        _(u"Thinking about your social network might help you go beyond a simplistic view of what your contacts are (who do you know?) and help you think about how the people in your company are connected to each other (your indirect contacts). The patterns of relations among people in your company, and your concrete position in those patterns, might allow you to access and procure valuable intangible assets, such as good advice, technical knowledge, emotional support, etc."),
        _(u"This report is based on the confidential information on your contact network collected with the web-based survey that you just completed. We analyzed your network to evaluate how your network may help you access important assets and organize them to achieve your professional goals. To improve the interpretation of your results, we compare them with the results of the other people in your group."),
        _(u"The report is organized in three parts. First, we analyze your network in terms of the number and the diversity of your contacts. Second, we analyze your network in terms of the kind and the strength of the relationships between you and your contacts. Third, we analyze the structure of your network, focusing on the patterns of relations among your contacts."),
    ),
)

captions = dict(
    nattrs = dict(
        age = _(u"This graph illustrates the distribution of your contacts by age. The age of your contacts is important because different generations have gone through different experiences that configure their opinions and their attitudes. The age of our contacts typically increases with age. This is natural, but also has draw-backs. A network can be a bridge across generations or it may amplify the natural separation between them."),
        functional_area = _(u"This graph illustrates the distribution of your contacts by their primary functional or professional area. It measures the extent to which your network reaches across functional boundaries. A network with contacts from different functional backgrounds exposes you to a richer picture of the business and allows you to learn about more opportunities to achieve your professional goals."),
        gender = _(u"This chart shows the gender distribution of your contacts. Gender diversity reveals your exposure to the view-points and experiences of the different sexes. This is partly defined by demographics since there are still significantly more men than women in most business settings. But it can be also driven by stereotypes: some men may find it difficult to build good professional relationships with women (and vice-versa)."),
        rank = _(u"The chart looks at the hierarchical diversity of your network. The diversity is your network in terms of rank is partly dependent on your own rank."),
        work = _(u"The graph above shows the proportion of contacts working in your same unit, in your same function (but in a different unit), in your same firm (but in a different function), and in other firms. It indicates the extent to which your network is limited to your own firm or office."),
    ),
    eattrs = dict(
        frequency = _(u"The chart displays the frequency with which you communicate with your contacts capturing your tendency to concentrate this communication on a specific time frame (e.g., on a weekly basis)."),
        helps = _(u"This graph represents how helpful your contacts are and the degree of supportiveness. Contacts with whom you have a long-lasting, frequent, and emotionally close relationship know you and your needs well. They are around to help when you need it, and they are more inclined to do so than weakly tied contacts."),
        strength = _(u"This graph represents the strength of the relationship with each contact in term of the closeness between you and the contact. Closer relationships might help you receive more support from your contacts."),
        context = _(u"This chart looks at the origin of your relationships. If most of our contacts come from one single source it is more likely that they will be similar in other aspects too."),
    ),
    structure = dict(
        density_cent = _(u"Network centralization vs. network density. The chart above plots both your results and the ones of the other survey respondents using their density and centralization scores. Density measures the proportion of direct ties in a network relative to the total number possible. The higher the centralization of your network, the more your network connectivity depends on one or few nodes that are connected with most people around you. The denser the network, the more all your contacts are connected with one another, and therefore your network is less likely to be centralized."),
        #order_size = "The chart above plots the networks in your reference group using their density and number of contacts.",
    ),
    egonet = dict( 
        neato = _(u"In this plot, you and your contacts are depicted as nodes linked through relations of different strength and nature. You are the bigger violet node. The light blue node is your boss. In red you have all the contacts with whom you maintained an adversarial relation (if any). The contacts with the green borders are the ones that you trust. The dashed green edges are the relations that help you the most. Your partner is depicted as an orange node. All other contacts are plotted as smaller light green nodes. The tie width represents the strength of the connection. All adversarial relations are plotted using a dashed red link."),
    )
)

