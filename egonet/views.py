from copy import copy

from django.views.generic import ListView, CreateView
from django.urls import reverse
from django.template import Context, RequestContext
from django.shortcuts import get_object_or_404,get_list_or_404, render
from django import http

from django.utils import timezone
from django.utils.translation import ugettext as _

from egonet.models import Group, Ego, Alter, Relationship
from egonet.figures import captions, sections, titles
from egonet.analysis import nattrs, eattrs
from egonet.choices import choices_dict
from egonet.questions import default_questions
from egonet.forms import (AddAltersForm, EgoForm, AlterForm, 
                            AlterNeighborsForm, RelationshipForm, 
                            StartForm, CompareAltersForm,)

def start(request):
    form = StartForm(request.POST or None)
    if request.POST and form.is_valid():
        group = form.login(request)
        if group:
            #request.session['groupuuid'] = group.groupuuid
            ego = Ego.objects.create(group=group, start_time=timezone.now())
            request.session['egouuid'] = str(ego.egouuid)
            request.session['questions'] = default_questions
            return http.HttpResponseRedirect('/explain/')
    # context for the template
    help_text = _("If you are having any trouble with the survey please <a href='mailto:acavicchini@iese.edu'>contact us</a>.")
    context = dict(
        title = _('Social Network Survey'), 
        description = sections['start_intro'],
        help_text = help_text,
        intro_survey = sections['intro_survey'],
        form = form
    )
    return render(request, 'start.html', context)

def add_ego(request):
    if 'egouuid' not in request.session:
        return http.HttpResponseRedirect('/start/')
    ego = get_object_or_404(Ego, egouuid=request.session['egouuid'])
    if not request.session['questions']:
        return http.HttpResponseRedirect('/start/') 
    questions = copy(request.session['questions'])
    question = dict(questions.pop(0))
    if request.method == 'POST':
        form = EgoForm(request.POST, instance=ego)
        if form.is_valid():
            ego = form.save()
            # redirect to the next question and set the question list
            # after poping this question
            request.session['questions'] = questions
            return http.HttpResponseRedirect(question['nexturl'])
    else:
        form = EgoForm(instance=ego)

    context = dict(
        title=question['title'],
        form=form,
        description=question['description'],
        )	
    return render(request, 'form.html', context)

def explain(request):
    if 'egouuid' not in request.session:
        return http.HttpResponseRedirect('/start/')
    ego = get_object_or_404(Ego, egouuid=request.session['egouuid'])
    if not request.session['questions']:
        return http.HttpResponseRedirect('/start/')
    questions = request.session['questions']
    question = dict(questions.pop(0))
    request.session['questions'] = questions
    context = dict(
        title=question['title'],
        nexturl=question['nexturl'],
        description=question['description'])
    return render(request, 'explanation.html', context)

def add_alters(request):
    if 'egouuid' not in request.session:
        return http.HttpResponseRedirect('/start/')
    ego = get_object_or_404(Ego, egouuid=request.session['egouuid'])
    if not request.session['questions']:
        return http.HttpResponseRedirect('/start/') 
    questions = copy(request.session['questions'])
    question = dict(questions.pop(0))
    if request.method == 'POST':
        form = AddAltersForm(request.POST, ego=ego)
        if form.is_valid():
            field = question['field']
            names = (v for k, v in form.cleaned_data.items()
                        if v and k != 'alters')
            for name in names:
                alter = Alter.objects.create(name=name, ego=ego)
                setattr(alter, field, True)
                alter.save()
            alters = form.cleaned_data.get('alters', None)
            print(alters)
            if alters is not None:
                for alter in alters:
                    setattr(alter, field, True)
                    alter.save()
            # redirect to the next question and set the question list
            # after poping this question
            request.session['questions'] = questions
            return http.HttpResponseRedirect(question['nexturl'])
    else:
        # This the the first page load, display a blank form
        # with as many new name fields as number
        number = question.get('number', 5)
        form = AddAltersForm(ego=ego, number=number)
    #PROVO A TIRARLO INDIETRO
    context = dict(
                title=question['title'],
                form=form,
                description=question['description']
                )
    return render(request, 'form.html', context)

def alters_info(request):
    if 'egouuid' not in request.session:
        return http.HttpResponseRedirect('/start/')
    ego = get_object_or_404(Ego, egouuid=request.session['egouuid'])
    if not request.session['questions']:
        return http.HttpResponseRedirect('/start/') 
    questions = copy(request.session['questions'])
    question = dict(questions.pop(0))
    alters = Alter.objects.filter(ego=ego, attrs_added=False)
    if not alters:
        # All alters done. 
        # Update the question list in session
        request.session['questions'] = questions
        # Redirect to the next block of questions.
        return  http.HttpResponseRedirect(question['nexturl'])
    else:
        # Redirect to the form for the next alter
        return  http.HttpResponseRedirect('/add_alter_info/%i/' % alters[0].id)

def add_alter_info(request, alter_id):
    alter = get_object_or_404(Alter, pk=alter_id)
    if request.method == 'POST':
        form = AlterForm(request.POST, instance=alter)
        if form.is_valid():
            attrs = form.save(commit=False)
            attrs.attrs_added = True
            attrs.save()
            # redirect to the 
            return http.HttpResponseRedirect('/alters_info/')
    else:
        form = AlterForm(instance=alter)
    context = dict(title=_('Information about: %s') % alter, form=form)
    return render(request, 'form.html', context)

def compare_alters(request):
    if 'egouuid' not in request.session:
        return http.HttpResponseRedirect('/start/')
    ego = get_object_or_404(Ego, egouuid=request.session['egouuid'])
    if not request.session['questions']:
        return http.HttpResponseRedirect('/start/') 
    questions = copy(request.session['questions'])
    question = dict(questions.pop(0))
    attr = question.get('attr')
    if attr not in choices_dict:
        return http.HttpResponseNotFound('<h1>Attribute %s not found!</h1>' % attr)
    if request.method == 'POST':
        form = CompareAltersForm(request.POST, ego=ego, attr=attr)
        if form.is_valid():
            field = question['field']
            for alter_field, value in form.cleaned_data.items():
                alter_id = int(alter_field.split('_')[1])
                alter = Alter.objects.get(pk=alter_id)
                setattr(alter, field, value)
                alter.save()
            # redirect to the next question and set the question list
            # after poping this question
            request.session['questions'] = questions
            return http.HttpResponseRedirect(question['nexturl'])
    else:
        # This the the first page load, display a blank form
        form = CompareAltersForm(ego=ego, attr=attr)
    context = dict(
        title=question['title'],
        form=form,
        description=question['description'],
        labels=[v for k, v in choices_dict[attr]],
    )
    return render(request, 'compare_form.html', context)

def alters_neighbors(request):
    if 'egouuid' not in request.session:
        return http.HttpResponseRedirect('/start/')
    ego = get_object_or_404(Ego, egouuid=request.session['egouuid'])
    if not request.session['questions']:
        return http.HttpResponseRedirect('/start/')
    questions = copy(request.session['questions'])
    question = dict(questions.pop(0))
    alters = Alter.objects.filter(ego=ego, neighbors_added=False)
    if not alters or len(alters) == 1:
        # All alters done. 
        # Update the question list in session
        request.session['questions'] = questions
        # Redirect to the next block of questions.
        return  http.HttpResponseRedirect(question['nexturl'])
    else:
        return  http.HttpResponseRedirect('/add_alter_neighbors/%i/' % alters[0].id)

def add_alter_neighbors(request, alter_id):
    alter = get_object_or_404(Alter, pk=alter_id)
    alter.neighbors_added = True
    alter.save()
    ego = alter.ego
    if request.method == 'POST':
        form = AlterNeighborsForm(request.POST, ego=ego)
        if form.is_valid():
            for nbr in form.cleaned_data.get('neighbors'):
                Relationship.objects.create(source=alter, target=nbr, ego=ego)
                Relationship.objects.create(source=nbr, target=alter, ego=ego)
            return http.HttpResponseRedirect('/alters_neighbors/')

    else:
        form = AlterNeighborsForm(ego=ego)
    context = dict(title=_('Identify the other contacts this person is connected to: %s') % alter, form=form)
    return render(request, 'form.html', context)

def relationships_attrs(request):
    if 'egouuid' not in request.session:
        return http.HttpResponseRedirect('/start/')
    ego = get_object_or_404(Ego, egouuid=request.session['egouuid'])
    if ego.completed:
        return  http.HttpResponseRedirect('/report/%s/' % ego.egouuid)
    if not request.session['questions']:
        return http.HttpResponseRedirect('/start/')
    questions = copy(request.session['questions'])
    question = dict(questions.pop(0))
    relationships = Relationship.objects.filter(ego=ego, attrs_added=False)
    if not relationships:
        # All alters done. 
        # Update the question list in session
        request.session['questions'] = questions
        # Redirect to the next block of questions.
        return  http.HttpResponseRedirect(question['nexturl'])
    else:
        return  http.HttpResponseRedirect('/add_relationship_attrs/%i/' % relationships[0].id)

def add_relationship_attrs(request, rel_id):
    rel = get_object_or_404(Relationship, pk=rel_id)
    if request.method == 'POST':
        form = RelationshipForm(request.POST, instance=rel)
        if form.is_valid():
            attrs = form.save(commit=False)
            attrs.attrs_added = True
            attrs.save()
            # Our relations are symetric and we have to maintain symetry by hand
            # for having relationship attributes: see models.ManyToMany("self", trought='')
            rev_rel = Relationship.objects.filter(source=attrs.target, target=attrs.source)
            rev_rel.strength = attrs.strength
            rev_rel.attrs_added = True
            rev_rel.save()
            return http.HttpResponseRedirect('/relationships_attrs/')
    else:
        form = RelationshipForm(instance=rel)
    desc = _("<p>This question is to assess how close are your contacts among them, using the following convention:</p><ul><li><strong>Very Close</strong>: They have a strong personal bond.</li><li><strong>Close</strong>: They feel close but do not have a strong personal bond.</li><li><strong>Neutral</strong>: They work OK with each other, but they have no personal bond.</li><li><strong>Distant</strong>: They'd rather avoid and will seek out only if necessary to work with each other.</li></ul>")
    context = dict(
        title=_("Can you qualify the relation between %s and %s") % (rel.source, rel.target),
        form=form,
        description=desc
    )
    return render(request, 'form.html', context)

def finished(request):
    if 'egouuid' not in request.session:
        return http.HttpResponseRedirect('/start/')
    ego = get_object_or_404(Ego, egouuid=request.session['egouuid'])
    ego.completed = True
    ego.end_time = timezone.now()
    ego.save()
    #TEST
    #to solve the neato not found in path we create the reports after
    #ego.make_plots()
    return  http.HttpResponseRedirect('/report/%s/' % ego.egouuid)

def report(request, egouuid):
    ego = get_object_or_404(Ego, egouuid=egouuid)
    # Start with the ego network plot
    egoplot = dict(
        title = "Your social network",
        text = sections['network'],
        path = "%s/%s" % (ego.get_ego_urldir(), 'egonet_neato.svg'),
    )
    # Node attributes
    n = len(ego.alter_set.all())
    node_attrs = []
    for attr in nattrs:
        node_attrs.append(
            dict(
                title = titles[attr] % n,
                text = captions['nattrs'][attr],
                path = "%s/%s" % (ego.get_ego_urldir(), attr + '.svg'),
            )
        )
    # Edge attributes
    edge_attrs = []
    for attr in eattrs:
        edge_attrs.append(
            dict(
                title = titles[attr] % n,
                text = captions['eattrs'][attr],
                path = "%s/%s" % (ego.get_ego_urldir(), attr + '.svg'),
            )
        )
    # Put every thing together
    context = dict(
        title = "%s's Social Network" % ego.name,
        description = sections['intro'],
        network = egoplot,
        node_intro = sections['node_attrs'],
        node_title = titles['node_attrs'],
        node_attrs = node_attrs,
        edge_intro = sections['edge_attrs'],
        edge_title = titles['edge_attrs'],
        edge_attrs = edge_attrs,
    )
  # HERE IS THE PROBLEM AND THE TEMPORARY SOLUTION
  # return render(request, 'report.html', context)
    return render(request, 'finished.html', context)

def sample_report(request):
    # Example report
    egoplot = dict(
        title = _("Your social network"),
        text = captions['egonet']['kk'],
        path = "%s/%s/%s" % ('egonet', 'example', 'egonet_kk.svg'),
    )
    # Node attributes
    n = 8
    node_attrs = []
    for attr in nattrs:
        node_attrs.append(
            dict(
                title = titles[attr] % n,
                text = captions['nattrs'][attr],
                path = "%s/%s/%s" % ('egonet', 'example', attr + '.svg'),
            )
        )
    # Edge attributes
    edge_attrs = []
    for attr in eattrs:
        edge_attrs.append(
            dict(
                title = titles[attr] % n,
                text = captions['eattrs'][attr],
                path = "%s/%s/%s" % ('egonet', 'example', attr + '.svg'),
            )
        )
    # Put every thing together
    context = dict(
        title = _('Sample Report'),
        description = sections['example_intro_short'],
        network = egoplot,
        node_intro = sections['node_attrs'],
        node_title = titles['node_attrs'],
        node_attrs = node_attrs,
        edge_intro = sections['edge_attrs'],
        edge_title = titles['edge_attrs'],
        edge_attrs = edge_attrs,
    )
    return render(request, 'sample_report.html', context)

def terms(request):
    context = dict(
        title = _('Usage terms and conditions'),
        description = _('nwebtools.com'),
    )
    return render(request, 'terms.html', context)