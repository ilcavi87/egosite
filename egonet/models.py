import os
import uuid
import types
from collections import defaultdict

import networkx as nx
import numpy as np
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField

from egonet import plots
from egonet import reports
from egonet.paths import REPORTS
from egonet.analysis import (nattrs, eattrs, mean, std, accumulate_attributes,
                            centralization_degree)
from egonet.choices import (GENDER_CHOICES, F_AREA_CHOICES, 
    EDUCATION_CHOICES, CURRENT_JOB_CHOICES, WORK_CHOICES, 
    RANK_CHOICES, FREQUENCY_CHOICES, STRENGTH_CHOICES,
    HELP_CHOICES, CONTEXT_CHOICES)#, SALARY_CHOICES)

GROUP_PLOT_DIR = "average"

def edges_not_to_ego(G):
    for u, v, d in G.edges(data=True):
        if not G.nodes[u]['is_ego'] and not G.nodes[v]['is_ego']:
            yield (u, v)

class Group(models.Model):

    name = models.CharField(max_length=255)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    password = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)

    groupuuid = models.CharField(max_length=50,
        default=uuid.uuid4,
        editable=False,
    )

    def get_groupdir(self):
        groupdir = os.path.join(
            REPORTS,
            "_".join([str(self.id), self.groupuuid]),
        )
        # If this group still does not have a directory, make it
        if not os.path.exists(groupdir):
            os.mkdir(groupdir)
        return groupdir

    def get_plotdir(self):
        plotdir = os.path.join(
            self.get_groupdir(),
            GROUP_PLOT_DIR,
        )
        # If this group still does not have a plot directory, make it
        if not os.path.exists(plotdir):
            os.mkdir(plotdir)
        return plotdir

    def get_group_urldir(self):
        urldir = os.path.join(
            os.path.basename(REPORTS),
            os.path.basename(self.get_groupdir()),
            GROUP_PLOT_DIR,
        )
        return urldir

    def generate_egonets(self):
        for ego in self.ego_set.filter(completed=True):
            yield ego.build_ego_network()

    def compute_reference_group_attributes(self):
        attr_results = dict((attr, {}) for attr in (nattrs + eattrs))
        for i, G in enumerate(self.generate_egonets()):
            for attr, result in attr_results.items():
                attr_results[attr] = accumulate_attributes(G, attr, result,
                                        nodes_or_edges='nodes' if attr in nattrs else 'edges')
        # divide by the total number of respondents
        for attr, result in attr_results.items():
            for k in result:
                result[k] /= float(i + 1)
        # Add the total number of respondents
        attr_results['n'] = i + 1
        return attr_results

    def make_attrs_plots(self):
        attrs = self.compute_reference_group_attributes()
        plotdir = self.get_plotdir()
        colors = plots.plot_average_pies(attrs, plotdir)
        return colors


    def compute_reference_group_metrics(self):
        metrics = defaultdict(list)
        for G in self.generate_egonets():
            metrics['centralization'].append(centralization_degree(G))
            metrics['density'].append(nx.density(G))
            metrics['order'].append(G.order())
            metrics['size'].append(G.size())
            ages = [v for v in nx.get_node_attributes(G,'age').values() if v]
            metrics['age'].append(mean(ages))
            metrics['age_std'].append(std(ages))
            times = [v for v in nx.get_node_attributes(G,'time_knowing').values() if v]
            metrics['time'].append(mean(times))
            metrics['time_std'].append(std(times))
        return dict(metrics)

    def build_reports(self):
        colors = self.make_attrs_plots()
        metrics = self.compute_reference_group_metrics()
        for ego in self.ego_set.filter(completed=True):
            ##DELETE THIS####
            #print(ego.first_name, " " , ego.last_name)
            ego.make_plots()
            ######
            ego.build_pdf_report(metrics=metrics, colors=colors)

    def export_egos_to_dir(self, path):
        for ego in self.ego_set.filter(completed=True):
            fname = os.path.join(path, "".join([ego.egouuid, '.graphml']))
            try:
                nx.write_graphml(ego.build_ego_network(), fname)
            except nx.NetworkXError:
                print(u"Error exporting %s" % ego)

    def import_egos_from_dir(self, path):
        for f in os.listdir(path):
            if f.endswith('.graphml'):
                try:
                    G = nx.read_graphml(os.path.join(path, f), node_type=types.UnicodeType)
                except Exception as e:
                    print(u"Error reading file %s" % f)
                    print(e)
                    continue
                if G.order() < 2 or G.size() == 0:
                    print(u"Emplty network at file %s" % f)
                    continue
                print(u"Adding Ego: %s" % next(n for n, d in G.nodes(data=True) if d['is_ego']))
                self.import_ego(G)


    def import_ego(self, G):
        """ G: a networkx Graph object """
        ego_node = next(n for n, d in G.nodes(data=True) if d['is_ego'])
        # Add ego
        if G.nodes[ego_node].get('first_name') is None:
            name_split = ego_node.split(' ')
            if len(name_split) > 1:
                first_name = name_split[0]
                last_name = name_split[-1]
            else:
                first_name = name_split[0]
                last_name = ''
        ego = Ego(
            group = self,
            first_name = G.nodes[ego_node].get('first_name') or first_name,
            last_name = G.nodes[ego_node].get('last_name') or last_name,
            age = G.nodes[ego_node].get('age'),
            gender = G.nodes[ego_node].get('gender'),
            nationality = G.nodes[ego_node].get('nationality'),
            email = G.nodes[ego_node].get('email'),
            education = G.nodes[ego_node].get('education'),
            company = G.nodes[ego_node].get('company'),
            functional_area = G.nodes[ego_node].get('functional_area'),
            #salary = G.nodes[ego_node].get('salary'),
            current_job = G.nodes[ego_node].get('current_job'),
            tenure = G.nodes[ego_node].get('tenure'),
            people_in_company = G.nodes[ego_node].get('people_in_company'),
            annual_sales = G.nodes[ego_node].get('annual_sales'),
            completed = True,
            start_time = G.nodes[ego_node].get('start_time'),
            end_time=None if G.nodes[ego_node]['end_time'] == 'Null' else G.nodes[ego_node]['end_time'],
            egouuid = G.nodes[ego_node].get('egouuid') or unicode(uuid.uuid4()),
        )

        ego.save()
        # Add alters
        for n in set(G) - set([ego_node]):
            alter = Alter.objects.create(
                ego = ego,
                name = n,
                age = G.nodes[n].get('age'),
                gender = G.nodes[n].get('gender'),
                nationality = G.nodes[n].get('nationality'),
                functional_area = G.nodes[n].get('functional_area'),
                attrs_added = True,
                neighbors_added = True,
                important_professional = G.nodes[n].get('important_professional'),
                important_career = G.nodes[n].get('important_career'),
                buyin = G.nodes[n].get('buyin'),
                hinder_professional = G.nodes[n].get('hinder_professional'),
                #evaluate_job_options = G.nodes[n].get('evaluate_job_options'),
                spend_free_time = G.nodes[n].get('spend_free_time'),
                life_partner = G.nodes[n].get('life_partner'),
                work = G.nodes[n].get('work'),
                rank = G.nodes[n].get('rank'),
                helps = G.nodes[n].get('helps'),
                time_knowing = G.nodes[n].get('time_knowing'),
                interaction = G.nodes[n].get('interaction'),
                strength = G.nodes[n].get('strength') if G.nodes[n].get('strength') \
                            else G.nodes[n].get('how_close'),
                context = G.nodes[n].get('context'),
                trust = G.nodes[n].get('trust'),
                reports_to_ego = G.nodes[n].get('reports_to_ego'),
                ego_reports_to = G.nodes[n].get('ego_reports_to'),
                alteruuid = G.nodes[n].get('alteruuid') or unicode(uuid.uuid4()),
            )
        # Add relationships among alters
        for u, v in edges_not_to_ego(G):
            source = Alter.objects.get(ego=ego, name=u)
            target = Alter.objects.get(ego=ego, name=v)
            strength = G.edge[u][v].get('strength')
            reluuid = G.edge[u][v].get('reluuid') or unicode(uuid.uuid4())
            Relationship.objects.create(
                source=source,
                target=target,
                ego=ego,
                strength=strength,
                reluuid=reluuid,
            )
            # We have to maintain symetry by hand because the DB definition is asymetric
            Relationship.objects.create(
                source=target,
                target=source,
                ego=ego,
                strength=strength,
                reluuid=reluuid,
            )
        # And finally make the plots for the imported ego
        this_ego = Ego.objects.get(pk=ego.id)
        this_ego.make_plots()

    def __str__(self):
        return self.name


class Ego(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE,)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)

    first_name = models.CharField(_("First Name"),
        max_length=255,
        null=True,
    )
    last_name = models.CharField(_("Last Name"), 
        max_length=255,    
        null=True,
    )

    age = models.IntegerField(_("Age"), null=True)
    gender = models.CharField(_("Gender"), 
        max_length=1, 
        choices=GENDER_CHOICES,
        null=True,
    )
    nationality = CountryField(_("Nationality"),
        null=True,
        help_text=_("If you have more than one, chose the one you identify with the most"),
    )
    email = models.EmailField(_("Email"), null=True)
    education = models.IntegerField(_("Eduaction"),
        choices=EDUCATION_CHOICES, 
        null = True,
        help_text=_("The highest level of formal education you have attained"),
    )
    #salary = models.IntegerField(_("Annual Salary"),
    #    choices=SALARY_CHOICES,
    #    null=True,
    #    help_text=_("Your annual salary in euros."),
    #)

    company = models.CharField(_("Company"),
        max_length=255,
        blank=True, 
        null=True,
        help_text=_("Company for which you currently work for"),
    )
    functional_area = models.IntegerField(_("Functional Area"), 
        choices=F_AREA_CHOICES, 
        null=True,
        help_text=_("Your primary functional area in the company"),
    )
    current_job = models.IntegerField(_("Current Job"), 
        choices=CURRENT_JOB_CHOICES,
        null=True,
    )
    tenure = models.FloatField(_("Tenure"), 
        blank=True, 
        null=True,
        help_text=_("Time you been working for this company."),
    )
    people_in_company = models.IntegerField(_("People in you company"), 
        blank=True, 
        null=True,
        help_text=_("People currently employed by your company. Provide your best estimate. Enter 1 if you are self-employed"),
    )
    annual_sales = models.FloatField(_("Annual Sales"), 
        blank=True, 
        null=True,
        help_text=_("Company annual sales in US$ Millions, your best estimate.")
    )
    
    completed = models.BooleanField(default=False)

    egouuid = models.CharField(max_length=50,
        default=uuid.uuid4,
        editable=False
    )

    def _get_name(self):
        """Use property for name"""
        return u'%s %s' % (self.first_name, self.last_name)
    name = property(_get_name)

    def get_egodir(self):
        egodir = os.path.join(
            self.group.get_groupdir(),
            self.egouuid,
        )
        # If this ego still does not have a directory, make it
        if not os.path.exists(egodir):
            os.mkdir(egodir)
        return egodir

    def get_ego_urldir(self):
        urldir = os.path.join(
            os.path.basename(REPORTS),
            os.path.basename(self.group.get_groupdir()),
            self.egouuid,
        )
        return urldir

    def total_time(self):
        if not self.end_time:
            return None
        delta = self.end_time - self.start_time
        return delta.seconds / 60.0

    def build_ego_network(self):
        G = nx.Graph()
        G.graph['name'] = u"{0}'s Ego Network".format(self.name)
        # Add ego to the network and add attributes
        G.add_node(self.name)
        G.nodes[self.name]['first_name'] = self.first_name
        G.nodes[self.name]['last_name'] = self.last_name
        G.nodes[self.name]['egouuid'] = self.egouuid
        G.nodes[self.name]['age'] = self.age
        G.nodes[self.name]['gender'] = self.gender
        G.nodes[self.name]['nationality'] = self.nationality.name.lower()
        G.nodes[self.name]['email'] = self.email
        G.nodes[self.name]['education'] = self.education
        G.nodes[self.name]['company'] = self.company or 'None'
        G.nodes[self.name]['functional_area'] = self.functional_area
        #G.nodes[self.name]['salary'] = self.salary
        G.nodes[self.name]['current_job'] = self.current_job
        G.nodes[self.name]['tenure'] = self.tenure or 0
        G.nodes[self.name]['people_in_company'] = self.people_in_company or 0
        G.nodes[self.name]['annual_sales'] = self.annual_sales or 0
        G.nodes[self.name]['start_time'] = self.start_time.strftime("%Y-%m-%d %H:%M:%S") \
                                            if self.start_time else 'Null'
        G.nodes[self.name]['end_time'] = self.end_time.strftime("%Y-%m-%d %H:%M:%S") \
                                            if self.end_time else 'Null'
        G.nodes[self.name]['is_ego'] = True
        # Add alters and their attributes
        #print(self.name)
        for alter in self.alter_set.all():
            # Add edge among ego and alters with attributes
            if alter.strength is None:
                alter.strength = 4
            G.add_edge(self.name, alter.name,
                        strength=alter.strength,
                        weight=5 - int(alter.strength),
                        frequency=alter.interaction,
                        time=alter.time_knowing,
                        context=alter.context,
                        helps=alter.helps,
                        boss=alter.ego_reports_to,
                        spouse=alter.life_partner,
                        important=alter.important_career,
                        hinders=alter.hinder_professional)
            # Add alter node attribute
            G.nodes[alter.name]['alteruuid'] = alter.alteruuid
            G.nodes[alter.name]['age'] = alter.age
            G.nodes[alter.name]['gender'] = alter.gender
            G.nodes[alter.name]['nationality'] = alter.nationality.name.lower()
            G.nodes[alter.name]['functional_area'] = alter.functional_area
            G.nodes[alter.name]['work'] = alter.work
            G.nodes[alter.name]['rank'] = alter.rank
            G.nodes[alter.name]['helps'] = alter.helps
            G.nodes[alter.name]['time_knowing'] = alter.time_knowing
            G.nodes[alter.name]['interaction'] = alter.interaction
            G.nodes[alter.name]['strength'] = alter.strength
            G.nodes[alter.name]['context'] = alter.context
            # Bolean attributes
            G.nodes[alter.name]['is_ego'] = False
            G.nodes[alter.name]['important_professional'] = alter.important_professional
            G.nodes[alter.name]['important_career'] = alter.important_career
            G.nodes[alter.name]['buyin'] = alter.buyin
            G.nodes[alter.name]['hinder_professional'] = alter.hinder_professional
            #G.nodes[alter.name]['evaluate_job_options'] = alter.evaluate_job_options
            G.nodes[alter.name]['spend_free_time'] = alter.spend_free_time
            G.nodes[alter.name]['life_partner'] = alter.life_partner
            G.nodes[alter.name]['trust'] = alter.trust
            G.nodes[alter.name]['reports_to_ego'] = alter.reports_to_ego
            G.nodes[alter.name]['ego_reports_to'] = alter.ego_reports_to
        # Finally add edges among alters with attributes
        for edge in self.relationship_set.all():
            G.add_edge(edge.source.name, edge.target.name,
                        strength=edge.strength,
                        # if strength was not set in the survey weight=2
                        weight=5 - int(edge.strength or 3),
                        reluuid=edge.reluuid)
        return G

    def make_plots(self):
        G = self.build_ego_network()
        egodir = self.get_egodir()
        plots.plot_pies(G, egodir)
        plots.plot_egonet(G, layout='neato',
            fname=os.path.join(egodir, "egonet-neato"))
        plots.plot_egonet(G, layout='circular', 
            fname=os.path.join(egodir, "egonet-circular"))
        plots.plot_egonet(G, layout='spring',
            fname=os.path.join(egodir, "egonet-spring"))
        plots.plot_egonet(G, layout='fdp',
            fname=os.path.join(egodir, "egonet-fdp"))

    def make_group_plots(self, metrics=None, colors=None):
        G = self.build_ego_network()
        if metrics is None:
            metrics = self.group.compute_reference_group_metrics()
        egodir = self.get_egodir()
        plots.plot_pies(G, egodir, colors=colors)
        plots.plot_bivariate(metrics, G, egodir)
        G = self.build_ego_network()
        plots.plot_egonet(G, layout='neato',
            fname=os.path.join(egodir, "egonet_kk"))

    def build_pdf_report(self, metrics=None, colors=None):
        reports.build_pdf_report(self, metrics=metrics, colors=colors)

    def get_pdf_path(self):
        egodir = self.get_egodir()
        report_path = os.path.join(egodir, 'report.pdf')
        if not os.path.exists(report_path):
            return None
        return report_path

    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.lower().capitalize()
            self.last_name = self.last_name.lower().capitalize()
        return super(Ego, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name.lower().capitalize() + " " + self.last_name.lower().capitalize()


class Alter(models.Model):

    ego = models.ForeignKey(Ego,on_delete=models.CASCADE,)
    #nbrs = models.ManyToManyField("self", blank=True, null=True)
    neighbors = models.ManyToManyField("self", through='Relationship', 
                                        symmetrical=False, 
                                        related_name='related_to+',
                                        blank=True)

    name = models.CharField(
        _("Name"),
        max_length=255,
    )
    age = models.IntegerField(_("Age"),
        blank=True,
        null=True, 
        help_text=_("If you are unsure, please provide your best guess"),
    )
    gender = models.CharField(_("Gender"),
        max_length=1, 
        choices=GENDER_CHOICES, 
        blank=True,
        null=True
    )
    nationality = CountryField(_("Nationality"),
        blank=True,
        null=True,
        help_text=_("If you are unsure, please provide your best guess")
    )
    functional_area = models.IntegerField(
        _("Functional Area"), 
        choices=F_AREA_CHOICES,
        blank=True,
        null=True)

    attrs_added = models.BooleanField(default=False)
    neighbors_added = models.BooleanField(default=False)

    important_professional = models.BooleanField(default=False)
    important_career = models.BooleanField(default=False)
    buyin = models.BooleanField(default=False)
    hinder_professional = models.BooleanField(default=False)
    #evaluate_job_options = models.BooleanField(default=False)
    spend_free_time = models.BooleanField(default=False)
    life_partner = models.BooleanField(default=False)
    
    work = models.IntegerField(_("Work"),
        choices=WORK_CHOICES,
        blank=True,
        null=True,
        help_text=_("Contact's workplace"),
    )
    rank = models.IntegerField(_("Rank"),
        choices=RANK_CHOICES,
        blank=True,
        null=True,
        help_text=_("Contact's formal rank in the organization he/she works for"),
    )
    helps = models.IntegerField(_("Helps"),
        choices=HELP_CHOICES,
        blank=True,
        null=True,
        help_text=_("Provides valuable help or technical advice to get my work done efficiently."),
    )
    time_knowing = models.FloatField(_("Time knowing"),
        blank=True,
        null=True,
        help_text=_("Time knowing this contact in years. You can enter fractions, such as 2.5 or 0.5"),
    )
    interaction = models.IntegerField(_("Interaction"), 
        choices=FREQUENCY_CHOICES,
        blank=True,
        null=True, 
        help_text=_("How often do you talk or exchange emails with this contact."),
    )
    strength = models.IntegerField(_("Strength of the relationship"), 
        choices=STRENGTH_CHOICES,
        blank=True,
        null=True,
        help_text=_("<strong>Very Close</strong>: Strong personal bond. <strong>Close</strong>: Feel close but without a strong personal bond. <strong>Neutral</strong>: This person is OK to work with, but no personal bond. <strong>Distant</strong>: Person you'd rather avoid and will seek out only if necessary."),
    )
    context = models.IntegerField(_("Context"), 
        choices=CONTEXT_CHOICES, 
        blank=True, 
        null=True,
        help_text=_("Context in which you first met this contact."),
    )

    trust = models.BooleanField(_("Trust"),
        default=False,
        help_text=_("Select if you would trust this contact for important personal matters."),
    )
    reports_to_ego = models.BooleanField(
        default=False,
        help_text=_("Select if the contact reports directly to you."),
    )
    ego_reports_to = models.BooleanField(
        default=False,
        help_text=_("Select if you report directly to the contact."),
    )

    alteruuid = models.CharField(max_length=50,
        default=uuid.uuid4,
        editable=False,
    )

    def save(self, *args, **kwargs):
        self.name = " ".join(w.capitalize() for w in self.name.lower().split())
        return super(Alter, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Relationship(models.Model):

    source = models.ForeignKey(Alter, related_name='source',on_delete=models.CASCADE,)
    target = models.ForeignKey(Alter, related_name='target',on_delete=models.CASCADE,)
    ego = models.ForeignKey(Ego,on_delete=models.CASCADE,)
    strength = models.IntegerField(choices=STRENGTH_CHOICES, blank=True, null=True)
    
    attrs_added = models.BooleanField(default=False)

    reluuid = models.CharField(max_length=50,
        default=uuid.uuid4,
        editable=False,
    )

    def __str__(self):
        return " ".join([self.source.name, '->', self.target.name])

