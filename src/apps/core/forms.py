from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .models import CustomUser, University


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        required=True,
        help_text='Required. Inform a valid email address.')
    #queryset for university and economical level
    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        required=True,
        help_text='Required. Select your university.')

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'university',
                  'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Email {email} already in use")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].strip()
        if not first_name:
            raise forms.ValidationError("First name is required")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name'].strip()
        if not last_name:
            raise forms.ValidationError("Last name is required")
        return last_name


class ProfileAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput,
                               required=True,
                               help_text="Required. Enter your password.")

	class Meta:
		model = CustomUser
		fields = ('email', 'password')
	
	def clean(self):
		if self.is_valid():
			email = self.cleaned_data.get('email')
			password = self.cleaned_data.get('password')
			if email and password:
				user = authenticate(email=email, password=password)
				if user is None:
					raise forms.ValidationError("Invalid email or password")


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=255, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not name:
            raise forms.ValidationError("Il nome è obbligatorio")
        return name
    
    def clean_message(self):
        message = self.cleaned_data['message'].strip()
        if not message:
            raise forms.ValidationError("Il messaggio è obbligatorio")
        return message
