from django import forms


class ReviewForm(forms.Form):
    stars = forms.IntegerField(min_value=1, max_value=5, required=True)
    comment = forms.CharField(widget=forms.Textarea, required=False)
