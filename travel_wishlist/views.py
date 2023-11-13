from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# @login_required will only allow the function to be called when someone is logged in.

# Default template to be shown an average user
@login_required()
def place_list(request):

    if request.method == 'POST':
        # Creates a place and adds it to the database if it is a valid entry.
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False)
        place.user = request.user
        if form.is_valid():
            place.save()
            return redirect('place_list')  # updates the home page

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()  # Used to create HTML form.
    return render(request, 'wishlist.html', {'places': places, 'new_place_form': new_place_form})


"""Gets all of the places in the database that HAVE BEEN visited to be displayed, using visited.html as a template for
formatting."""
@login_required()
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'visited.html', {'visited': visited})


"""This function changes the status of a place from unvisited TO visited, and makes a change to the database entry.
Error handling for nonexistent locations is present. It will also check if the place's owner is the one trying to 
change its visited status, and will stop the change if they are not."""
@login_required()
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list')


"""Sends back a formatted About page with about.html as the format, and author information."""
def about(request):
    author = 'Zion Nichols'
    about = 'A website to create a list of places you want to visit.'
    return render(request, 'about.html', {'author': author, 'about': about})


"""Sends the user to the details page for a place, which says whether the place has been visited, a button to make it
visited if it hasn't been, and a delete button to remove the place entirely."""
@login_required()
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    return render(request, 'place_detail.html', {'place': place})


"""This will delete a place from a user's wishlist. If the requester is that the same person that added the place, the
place will not be deleted."""
@login_required()
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden
