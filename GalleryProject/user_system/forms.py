from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from phonenumber_field.modelfields import PhoneNumberField
from django import forms


reg_contact_method = [
    'Email',
    'Text',
    'Call'
]

group_list = []
query_group_list = Group.objects.all().values_list('name', 'name')

for group in query_group_list:
    group_list.append(group)

class RegForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone = forms.CharField()
    hexkey = forms.CharField(max_length=255)

    address_1 = forms.CharField(max_length=255)
    address_2 = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    state = forms.CharField(max_length=255)
    zip_code =forms.CharField(max_length=255)
    
    class Meta:
        model = User
        fields = ('username', 'hexkey','phone','address_1','address_2','city', 'state', 'zip_code','first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['hexkey'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['address_1'].widget.attrs['class'] = 'form-control'
        self.fields['address_2'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['state'].widget.attrs['class'] = 'form-select'
        self.fields['zip_code'].widget.attrs['class'] = 'form-control'
        
        
        
        
class LoginForm():
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('username', 'password')



class ProfileForm(UserChangeForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')