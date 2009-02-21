from django import forms
from django.contrib.admin import widgets as admin_widgets
from django.contrib.auth.models import User

from gazjango.articles.models      import StoryConcept
from gazjango.accounts.models      import UserProfile


# note that this form should be saved manually (with commit=False)
class SubmitStoryConcept(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(SubmitStoryConcept, self).__init__(*args, **kwargs)
    
    class Meta:
        model = StoryConcept
        fields = ('name','due')
    
class ConceptSaveForm(forms.Form):
    name = forms.CharField(label = 'Concept',   widget=forms.TextInput(attrs={'size': 64}), required=True)
    notes= forms.CharField(label = 'Notes',     widget=forms.Textarea( attrs={'cols': 65}), required=True)
    due  = forms.CharField(label = 'Due Date',  widget=forms.TextInput(attrs={'size': 15})               )
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=admin_widgets.FilteredSelectMultiple)
    
    
    users = forms.MultipleChoiceField(
        
    )
    
    departments = forms.MultipleChoiceField(
        widget=admin_widgets.FilteredSelectMultiple('departments', False),
        required=False
    )
    self.fields['departments'].choices = [
        (tag.pk, tag.longest_name())
        for tag in departments_taggroup().tags.all()
    ]