from urllib import request
from django import forms
from django.core.files.base import ContentFile

from .models import Image
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        # Użytkownicy nie będą wprowadzać adresu URL w formularzu, zamiast tego otrzymają narzędzie JS pozwalające na
        # wybranie obrazu z zewnętrznej witryny, a jego adres URL będzie przekazany jako prarametr naszemu formularzowi.
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        # Dzielimy adres url w celu otrzymania rozszerzenia pliku i sprawdzenia (valid_extensions).
        # Jeżeli rozszerzenie nie znajduję się w valid_extensions następuje zgłoszenie wyjątku ValidationError.
        extension = url.rsplit('.', 1)[1].lower()
        # e.g. "https://jakastamstrona.com/image/thumb/jakistamobraz.jpg" - extension dzieli url na liste z dwoma
        # elementami. Jeżeli ostatni element zawiera valid_extensions metoda zwróci url.
        if extension not in valid_extensions:
            raise forms.ValidationError('Podany adres URL nie zawieta obrazów w obsługiwanym formacie.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.',1)[1].lower())
        # Pobranie pliku obrazu z podanego adresu URL.
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image