from django import forms
from .models import Client, Invite, Project, ProjectTerms, ProjectRequest, RequestReply
from phonenumber_field.modelfields import PhoneNumberField

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
class InviteForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ('name', 'email')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        fields = ('name', 'date', 'scope', 'details', 'location')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'scope': forms.Select(attrs={'class': 'form-select'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
        }
        
class RequestReplyComment(forms.ModelForm):
    class Meta:
        model = RequestReply
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProjectTermsForm(forms.ModelForm):
    class Meta:
        model = ProjectTerms
        fields = ('project_cost',
                  'deposit',
                  'services'
                  )
        
        widgets = {
            'project_cost': forms.TextInput(attrs={'class': 'form-control'}),
            'deposit': forms.TextInput(attrs={'class': 'form-control'}),
            'services': forms.Textarea(attrs={'class': 'form-control'}),
        }