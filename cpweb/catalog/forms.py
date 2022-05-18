from django import forms
from django.core.exceptions import ValidationError


class TasteForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': "buy-count", 'name': "count"}),
        label="",
        initial=1,
        min_value=0,
        required=True
    )

    def clean_quantity(self):
        num = self.cleaned_data['quantity']
        if type(num) != int:
            raise ValidationError('Need to be integer number')
        return num
