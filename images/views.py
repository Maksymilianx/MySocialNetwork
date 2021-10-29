from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from images.forms import ImageCreateForm


@login_required
def image_create(request):
    if request.method == 'POST':
        # Formularz został wysłany:
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # Dane formularza są prawidłowe.
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # Przypisano bieżącego użytkownika do elementu.
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Obraz został dodany.')
            # Przekierowanie do widoku szczegółowego dla nowo utworzonego elementu.
            return redirect(new_item.get_absolute_url())
        else:
            # Utworzenie formularza na podstawie danych dostarczonych przez MySocialNetwork w żądaniu GET.
            form = ImageCreateForm(data=request.GET)
        return render(request, 'images/image/create.html', {'section': 'images', 'form': form})