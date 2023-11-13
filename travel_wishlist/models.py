from django.db import models
from django.contrib.auth.models import User

"""Place object used to link a place's name and whether it's been visited. Also has a user's key to allow for user-specific
 wish lists, when they may have visited the place, notes on said place, and a photo if one is available."""
class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True,  null=True)

    # Gives basic info on a place, such as who added it, its name, and details if possible. Not intended to be seen by users.
    def __str__(self):
        photo_str = self.photo.url if self.photo else 'No photo found.'
        notes_str = self.notes[100:] if self.notes else 'No notes.'
        return f'{self.pk}: {self.name} visited? {self.visited} on {self.date_visited}\nPhoto {photo_str}'
