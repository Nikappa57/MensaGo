from django import forms

from apps.core.models import CustomUser

class AllergensForm(forms.Form):
    suffers_from = forms.ModelMultipleChoiceField(
        queryset=CustomUser._meta.get_field('suffers_from').related_model.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        help_text='Select allergens'
    )


class ProfileForm(forms.ModelForm):
    suffers_from = forms.ModelMultipleChoiceField(
        queryset=CustomUser._meta.get_field('suffers_from').related_model.objects.all(), # TODO: ma mettere direttamente il modello no?
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '8'}),
        help_text='Select allergens'
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'university', 'economical_level', 'propic', 'suffers_from']
        widgets = {
            'propic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

