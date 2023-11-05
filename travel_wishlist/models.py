from django.db import models

"""Place object used to link a place's name and whether it's been visited. """
class Place(models.Model):
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

    # Gives basic info on a place and whether the user has visited it. Not intended to be seen by users.
    def __str__(self):
        return f'{self.name} visited? {self.visited}'
