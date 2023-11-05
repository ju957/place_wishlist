from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Default template to be shown an average user
def place_list(request):

    if request.method == 'POST':
        # Creates a place and adds it to the database if it is a valid entry.
        form = NewPlaceForm(request.POST)
        place = form.save()
        if form.is_valid():
            place.save()
            return redirect('place_list')  # updates the home page

    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()  # Used to create HTML form.
    return render(request, 'wishlist.html', {'places': places, 'new_place_form': new_place_form})


def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'visited.html', {'visited':visited})

def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()

    return redirect('place_list')


def about(request):
    author = 'Zion Nichols'
    about = 'A website to create a list of places you want to visit.'
    return render(request, 'about.html', {'author': author, 'about': about})