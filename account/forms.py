from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
import regex as re

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is invalid')
        
        if len(email) > 350:
            raise forms.ValidationError('This email is too long')
        
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Check if username is empty
        if not username:
            raise forms.ValidationError('This field is required.')

        # Check if username contains only numbers
        if username.isdigit():
            raise forms.ValidationError('Username cannot contain only numbers.')

        # Ensure username length is reasonable
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        if len(username) > 150:
            raise forms.ValidationError('Username must not exceed 150 characters.')

        # Restrict special characters
        if not re.match(r'^[\w.@+-]+$', username):
            raise forms.ValidationError(
                'Username may only contain letters, digits, and @/./+/-/_ characters.')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already in use.')

        return username
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email']:
            self.fields[fieldname].help_text = None

        self.fields['email'].required = True

        self.fields['email'].widget.attrs.update({
            'readonly': 'readonly',
            'class': 'form-control readonly-field',  # Optional class for styling
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is invalid')
        
        if len(email) > 350:
            raise forms.ValidationError('This email is too long')
        
        return email