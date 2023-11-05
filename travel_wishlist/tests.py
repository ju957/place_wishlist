from django.test import TestCase
from django.urls import reverse
from .models import Place


class TestHomePage(TestCase):
    """This test checks whether the home page displays the no places message with an empty database."""
    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        self.assertTemplateUsed('travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist')


class TestWishList(TestCase):
    fixtures = ['test_places']  # test data stored in the fixtures directory (json type data)

    """This test individually checks each test place, and whether it  is/isn't displayed on the home page. Displayed
       means it hasn't been visited."""
    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed('travel_wishlist/wishlist.html')

        self.assertContains(response, 'Tokyo')  # Should be displayed
        self.assertContains(response, 'New York')

        self.assertNotContains(response, 'San Francisco')  # Should NOT be displayed
        self.assertNotContains(response, 'Moab')


class TestVisitedPage(TestCase):
    """This test checks whether the visited place page displays the no places message with an empty database."""
    def test_visited_page_shows_empty_list_message_for_empty_database(self):
        visited_page_url = reverse('places_visited')
        response = self.client.get(visited_page_url)
        self.assertTemplateUsed('travel_wishlist/visited.html')
        self.assertContains(response, 'You haven\'t visited any places yet.')


class TestVisitedList(TestCase):
    fixtures = ['test_places']  # test data stored in the fixtures directory (json type data)

    """This test individually checks each test place, and whether it  is/isn't displayed on the visited page. This page
    should display everything that HAS BEEN visited."""
    def test_visited_list_contains_visited_places(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed('travel_wishlist/visited.html')
        self.assertNotContains(response, 'Tokyo')  # Should NOT be present
        self.assertNotContains(response, 'New York')

        self.assertContains(response, 'San Francisco')  # Should be displayed
        self.assertContains(response, 'Moab')


class TestAddNewPlace(TestCase):
    """This test checks what happens when a place is attempted to be added to the unvisited place list.
    The correct response should be the place being found in the database."""
    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}

        response = self.client.post(add_place_url, new_place_data, follow=True)

        self.assertTemplateUsed(response, 'wishlist.html')

        response_places = response.context['places']
        self.assertEqual(1, len(response_places))
        tokyo_from_response = response_places[0]

        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False)  # Searches the database for Tokyo.

        self.assertEqual(tokyo_from_database, tokyo_from_response)

class TestVisitPlace(TestCase):
    fixtures = ['test_places']  # test data stored in the fixtures directory (json type data)
    """This test uses test data to check if the code that changes a place to visited works. After changing New York to
    visited, it checks whether New York was removed from the homepage, and then checks another place to see if places
    are being displayed at all."""
    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2, ))  # argument is pk 2, New York

        response = self.client.post(visit_place_url, follow=True)

        self.assertTemplateUsed(response, 'wishlist.html')

        self.assertNotContains(response, 'New York')  # Should no longer be on the homepage
        self.assertContains(response, 'Tokyo')  # Unchanged, control variable test.

        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)  # Makes sure the New York place was properly changed.

    """This test checks the response of the code that changes a place to visited if you send a pk that isn't
    present in the database. The response should be a 404 error, request not found."""
    def test_nonexistent_place(self):
        visit_nonexistent_place_url = reverse('place_was_visited', args=(123456, ))
        response = self.client.post(visit_nonexistent_place_url, follow=True)
        self.assertEqual(404, response.status_code)