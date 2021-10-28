from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Image(models.Model):
    # Użytkownik może dodać wiele obrazów, ale każdy obraz może być dodany tylko przez jednego użytkownika.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # Slug - krótka etykieta wykorzystywana do przygotowania ładnych adresów URL
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    # created - data i godzina utworzenia obiektu w db. auto_now_add - wartość daty i godziny ustawiana jest automatycznie
    # podczas tworzenia obiektu. db_index=True - Django tworzy indeks w db dla tej kolumny
    # Indeksy w bazach poprawiają wydajność wykonywania zapytań. Zaleca się używać opcję db_index=True dla kolumn,
    # które są często wykorzystywane w zapytaniach za pomocą funkcji filter(), exclude(), order_by().
    created = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    # metoda save utworzona jest w celu auto. wygenerowania wartości do kolumny slug na podstawie wartości pola title.
    def save(self, *args, **kwargs):
        if not self.slug:
            # jeżeli wartość kolumny slug nie zostanie podana, funkcja slugify generuje dla obrazu wartość kolumny slug.
            self.slug = slugify(self.title)
            # obiekt zostaje zapisany, a wartości kolumny slug będą generowane automatycznie, aby user nie musiał robić
            # tego ręcznie dla każdego obrazu.
            super().save(*args, **kwargs)