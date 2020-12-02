from django import forms
from .models import User


class RegisterForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)
    confirmation = forms.CharField(required=True)
    gender = forms.ChoiceField(required=True)
    choices = (('2.5', '2.5'), ('3.0', '3.0'), ('3.5', '3.5'), ('4.0', '4.0'), ('4.5', '4.5'), ('5.0', '5.0'))
    level = forms.ChoiceField(
        widget=forms.Select(),
        choices=choices,
        required=True
    )
    singles = forms.BooleanField()
    doubles = forms.BooleanField()
    mixed_doubles = forms.BooleanField()
    picture = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmation', 'gender', 'level', 'singles', 'doubles', 'mixed_doubles',
                  'picture']
