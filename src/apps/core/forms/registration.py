from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.safestring import mark_safe

from apps.core.models import CustomUser, University, EconomicalLevel


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Form personalizzato per il cambio password che aggiunge stile alle classi
    """
    old_password = forms.CharField(
        label="Password attuale",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    new_password1 = forms.CharField(
        label="Nuova password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    new_password2 = forms.CharField(
        label="Conferma nuova password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

class RegistrationForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Override form-level password mismatch message
		self.error_messages['password_mismatch'] = 'Le due password non coincidono.'

	email = forms.EmailField(
		max_length=255,
		required=True,
		help_text='Inserisci un indirizzo email valido.',
		error_messages={
			'required': "L'email è obbligatoria.",
			'invalid': "Inserisci un indirizzo email valido.",
			'unique': "Questa email è già in uso.",
		}
	)
	
	first_name = forms.CharField(
		max_length=255,
		required=True,
		help_text='Inserisci il tuo nome.',
		error_messages={
			'required': "Il nome è obbligatorio.",
		}
	)

	last_name = forms.CharField(
		max_length=255,
		required=True,
		help_text='Inserisci il tuo cognome.',
		error_messages={
			'required': "Il cognome è obbligatorio.",
		}
	)

	propic = forms.ImageField(
		required=False,
		help_text='Carica una foto profilo (opzionale).',
		error_messages={
			'invalid_image': "Il file caricato non è un'immagine valida.",
		}
	)

	university = forms.ModelChoiceField(
		queryset=University.objects.all(),
		required=True,
		help_text='Seleziona la tua università.',
		error_messages={
			'required': "La selezione dell'università è obbligatoria.",
			'invalid_choice': "L'università selezionata non è valida."
		}
	)
	economical_level = forms.ModelChoiceField(
		queryset=EconomicalLevel.objects.all(),
		required=False,
		help_text='Seleziona il tuo livello economico.',
		error_messages={
			'invalid_choice': "Livello economico non valido."
		}
	)

	# Override dei campi password per help_text in italiano
	password1 = forms.CharField(
		label="Password",
		widget=forms.PasswordInput,
		required=True,
		min_length=8,
		help_text=mark_safe(
			'La password deve rispettare le seguenti regole:'
			'<ul>'
			'<li>Minimo 8 caratteri</li>'
			'<li>Non troppo simile alle informazioni personali</li>'
			'<li>Non può essere una password comunemente utilizzata</li>'
			'<li>Non può contenere solo numeri</li>'
			'</ul>'
		),
		error_messages={
			'required': "La password è obbligatoria.",
			'min_length': "La password deve avere almeno 8 caratteri.",
			'invalid': "La password non è valida.",
		}
	)
	password2 = forms.CharField(
		label="Conferma password",
		widget=forms.PasswordInput,
		required=True,
		min_length=8,
		help_text='Reinserisci la password per conferma.',
		error_messages={
			'required': "La conferma della password è obbligatoria.",
			'min_length': "",

		}
	)

	# Campo per i termini di servizio
	terms_accepted = forms.BooleanField(
		required=True,
		error_messages={
			'required': "Devi accettare i termini di servizio per registrarti.",
		}
	)

	class Meta:
		model = CustomUser
		fields = (
			'email', 'first_name', 'last_name', 'propic',
			'university', 'economical_level',
			'password1', 'password2'
		)

	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data['email']
		user.economical_level = self.cleaned_data.get('economical_level')
		if self.cleaned_data.get('propic'):
			user.propic = self.cleaned_data['propic']
		if commit:
			user.save()
		return user

	def clean_email(self):
		email = self.cleaned_data['email'].lower().strip()
		if CustomUser.objects.filter(email=email).exists():
			raise forms.ValidationError(f"L'email {email} è già in uso")
		return email

	def clean_first_name(self):
		first_name = self.cleaned_data['first_name'].strip()
		if not first_name:
			raise forms.ValidationError('Il nome è obbligatorio')
		return first_name

	def clean_last_name(self):
		last_name = self.cleaned_data['last_name'].strip()
		if not last_name:
			raise forms.ValidationError('Il cognome è obbligatorio')
		return last_name

# TODO: perchè non CustomLoginForm?
class ProfileAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label="Password",
							   widget=forms.PasswordInput,
							   required=True,
							   help_text="Obbligatorio. Inserisci la tua password.")

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
					raise forms.ValidationError('Email o password non validi')



class CustomPasswordChangeForm(PasswordChangeForm):
	"""
	Form personalizzato per il cambio password che aggiunge stile alle classi
	"""
	def __init__(self, user, *args, **kwargs):
		super().__init__(user, *args, **kwargs)
		# Override form-level and field-level messages in Italian
		self.error_messages['password_mismatch'] = 'Le due password non coincidono.'
		self.error_messages['password_incorrect'] = 'La password attuale non è corretta.'
		# Ensure `old_password` field uses custom incorrect-password message
		self.fields['old_password'].error_messages['password_incorrect'] = 'La password attuale non è corretta.'
 	


	old_password = forms.CharField(
 		label="Password attuale",
 		widget=forms.PasswordInput(attrs={'class': 'form-control'}),
 		required=True,
 		error_messages={
 			'required': 'Il campo password attuale è obbligatorio.',
 			'invalid': 'La password attuale non è corretta.',
 		}
 	)
	new_password1 = forms.CharField(
		label="Nuova password",
		widget=forms.PasswordInput(attrs={'class': 'form-control'}),
		required=True, 
		min_length=8,
		help_text=mark_safe(
			'<ul>'
			'<li>Minimo 8 caratteri</li>'
			'<li>Non troppo simile ai tuoi dati personali</li>'
			'<li>Non può essere una password comune</li>'
			'<li>Non può contenere solo numeri</li>'
			'</ul>'
		),
		error_messages={
			'required': "La password è obbligatoria.",
			'min_length': "La password deve avere almeno 8 caratteri.",
			'invalid': "La password non è valida.",
		}
	)
	new_password2 = forms.CharField(
		label="Conferma nuova password",
		widget=forms.PasswordInput(attrs={'class': 'form-control'}),
		required=True,
		min_length=8,
		help_text='Reinserisci la password per conferma.',
		error_messages={
			'required': 'La conferma della password è obbligatoria.',
			'min_length': "",
			'password_mismatch': 'Le due password non coincidono.'
		}
	)


class CustomPasswordResetForm(PasswordResetForm):
	email = forms.EmailField(
		max_length=254,
		required=True,
		help_text='Inserisci l’email con cui sei registrato.',
		error_messages={
			'required': 'Il campo email è obbligatorio.',
			'invalid': 'Inserisci un indirizzo email valido.'
		}
	)


class CustomSetPasswordForm(SetPasswordForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.error_messages['password_mismatch'] = 'Le due password non coincidono.'


	new_password1 = forms.CharField(
		label='Nuova password',
		widget=forms.PasswordInput,
		required=True,
		min_length=8,
		help_text=mark_safe(
			'<ul>'
			'<li>Minimo 8 caratteri</li>'
			'<li>Non troppo simile ai tuoi dati personali</li>'
			'<li>Non può essere una password comune</li>'
			'<li>Non può contenere solo numeri</li>'
			'</ul>'
		),
		error_messages={
			'required': 'La password è obbligatoria.',
			'min_length': 'La password deve avere almeno 8 caratteri.',
			'password_mismatch': 'Le due password non coincidono.',
			'invalid': "La password non è valida.",
		}
	)

	new_password2 = forms.CharField(
		label='Conferma nuova password',
		widget=forms.PasswordInput,
		required=True,
		min_length=8,
		help_text='Reinserisci la password per conferma.',
		error_messages={
			'required': 'La conferma della password è obbligatoria.',
			'password_mismatch': 'Le due password non coincidono.',
			'min_length': "",

		}
	)
