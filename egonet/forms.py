from django import forms
from django.utils import timezone

from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from egonet.models import Alter, Ego, Group, Relationship
from egonet.choices import choices_dict, GENDER_CHOICES

class StartForm(forms.Form):

#    accept = forms.BooleanField(
#        label=_("I accept the <a href='/terms/'>terms and conditions</a>."),
#        help_text=_("I accept the terms and conditions"), 
#        required=True,
#    )
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
#        accept = self.cleaned_data.get('accept')
#        if not accept:
#            raise forms.ValidationError(
#                    _("You have to accept terms and conditions to start the survey"),
#            )
        password = self.cleaned_data.get('password')
        try:
            group = Group.objects.get(password=password)
            if group.end_date < timezone.now():
                raise forms.ValidationError(
                    _("Sorry, this survey group is closed since %s") % group.end_date.strftime(
                                                                        "%A, %d %B %Y %H:%M:%S"))
        except Group.DoesNotExist: 
            raise forms.ValidationError(_("Sorry, that password was invalid. Please try again."))
        return self.cleaned_data

    def login(self, request):
        password = self.cleaned_data.get('password')
        group = Group.objects.get(password=password)
        return group


class AddAltersForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.ego = kwargs.pop('ego')
        if 'number' not in kwargs:
            number = 5
        else:
            number = int(kwargs.pop('number'))
        super(AddAltersForm, self).__init__(*args, **kwargs)
        #alters = Alter.objects.filter(ego=ego)
        if Alter.objects.filter(ego=self.ego):
            self.fields['alters'] = forms.ModelMultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                queryset=Alter.objects.filter(ego=self.ego),
                required=False,
                label=_('Select a contact'),
            )
        for i in range(number):
            self.fields['name_%s' % i] = forms.CharField(
                max_length=255, 
                required=False, 
                label=_('Add new contact'),
            )

    def clean(self):
        names = [v for k, v in self.cleaned_data.items()
                            if v and k != 'alters']

        if len(names) != len(set(names)):
            raise forms.ValidationError(
                    _('Please, do not use the same name for two contacts.')
                )
        for alter in self.ego.alter_set.all():
            if alter.name in names:
                raise forms.ValidationError(
                        _('Please, do not use the same name for two contacts. You can select contacts already mentioned in the form below.')
                )

        return self.cleaned_data


class AlterNeighborsForm(forms.Form):

    neighbors = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                queryset=Alter.objects.all(),
                                                required=False,
                                                label=_('Select relations'))

    def __init__(self, *args, **kwargs):
        ego = kwargs.pop('ego')
        super(AlterNeighborsForm, self).__init__(*args, **kwargs)
        self.fields['neighbors'].queryset = Alter.objects.filter(ego=ego, neighbors_added=False)


class HorizontalRadioRenderer(forms.RadioSelect):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

#widget=forms.RadioSelect(renderer=HorizontalRadioRenderer),


class CompareAltersForm(forms.Form):

    def __init__(self, *args, **kwargs):
        ego = kwargs.pop('ego')
        attr = kwargs.pop('attr')
        super(CompareAltersForm, self).__init__(*args, **kwargs)
        for alter in Alter.objects.filter(ego=ego):
            self.fields['alter_%s' % alter.id] = forms.ChoiceField(
                choices=choices_dict[attr], 
                widget=forms.RadioSelect,
#widget=forms.RadioSelect(),
                label=alter.name,
            )
            self.fields['alter_%s' % alter.id].required = True

    def clean(self):
        if not (len(self.fields) == len([v for v in self.cleaned_data.values()])):
            raise forms.ValidationError(
                _('Please, complete information for all contacts.'),
            )
        return self.cleaned_data


class EgoForm(forms.ModelForm):

    class Meta:
        model = Ego
        exclude = (
            'group',
            'alters',
            'completed',
            'egouuid',
            'start_time',
            'end_time',
            'people_in_company',
            'annual_sales',
        )


class AlterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AlterForm, self).__init__(*args, **kwargs)
        self.fields['nationality'].required = True
        self.fields['age'].required = True
        self.fields['time_knowing'].required = True
        self.fields['gender'].required = True
        self.fields['gender'].widget = forms.RadioSelect(choices=GENDER_CHOICES)

    class Meta:
        model = Alter
        fields = (
            'age', 
            'gender', 
            'nationality', 
            'time_knowing',
            'trust',
        )

class RelationshipForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RelationshipForm, self).__init__(*args, **kwargs)
        self.fields['strength'].required = True
        self.fields['strength'].widget = forms.RadioSelect(choices=choices_dict['strength'])

    class Meta:
        model = Relationship
        exclude = ['source', 'target', 'ego', 'attrs_added']


