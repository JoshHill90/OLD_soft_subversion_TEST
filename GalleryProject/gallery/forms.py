from django import forms
from .models import Image
from django.forms import MultipleChoiceField, ChoiceField, Form

class ImageForms(forms.ModelForm):

    class Meta:
        
        
        model = Image
        fields = ('title','tag', 'display', 'client_id', 'project_id')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title for the post'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'display': forms.Select(attrs={'class': 'form-select', 'multiple': True}),                                
            'client_id': forms.Select(attrs={'class': 'form-select'}),
            'project_id': forms.Select(attrs={'class': 'form-select'}),                             
        }