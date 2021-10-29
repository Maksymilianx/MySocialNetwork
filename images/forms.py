from django import forms
from .models import Image

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        # Użytkownicy nie będą wprowadzać adresu URL w formularzu, zamiast tego otrzymają narzędzie JS pozwalające na
        # wybranie obrazu z zewnętrznej witryny, a jego adres URL będzie przekazany jako prarametr naszemu formularzowi.
        widgets = {
            'url': forms.HiddenInput,
        }