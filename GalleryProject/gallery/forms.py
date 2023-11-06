from django import forms
from .models import Image


class ImageForms(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title','tag', 'private', 'display', 'portrait_format', 'client_id', 'project_id','cloudflare_id')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title for the post'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'private': forms.CheckboxInput(attrs={'type': 'checkbox',
                                                  'class': 'form-check-input',
                                                  'id': 'flexSwitchCheckChecked',
                                                  }),
            'display': forms.Select(attrs={'class': 'form-control'}), 
            'portrait_format': forms.Select(attrs={'class': 'form-control'}),                                       
            'client_id': forms.Select(attrs={'class': 'form-control'}),
            'project_id': forms.Select(attrs={'class': 'form-control'}),
            'cloudflare_id': forms.TextInput(attrs={'class': 'form-control'}),                              
        }