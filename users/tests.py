"""Test cases for users app."""
from django.utils import timezone
from rest_framework.test import APITestCase
from events.models import Event
from bodies.models import Body
from login.tests import get_new_user

class UserTestCase(APITestCase):
    """Unit tests for users."""

    user = None
    test_body = None

    def setUp(self):
        # Fake authenticate
        self.user = get_new_user()
        self.client.force_authenticate(self.user) # pylint: disable=E1101
        self.test_body = Body.objects.create(name="test")

    def test_user_me(self):
        """Check the /api/user-me API."""

        # Check GET
        url = '/api/user-me'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], str(self.user.profile.id))

        # Check PATCH
        url = '/api/user-me'
        data = {
            "followed_bodies_id": [str(self.test_body.id)]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.profile.followed_bodies.all()[0], self.test_body)

        event = Event.objects.create(
            start_time=timezone.now(), end_time=timezone.now(), created_by=self.user.profile)

        # Check marking interested
        url = '/api/user-me/ues/' + str(event.id) + '?status=1'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(event.followers.all()[0], self.user.profile)
        url = '/api/user-me'
        response = self.client.get(url, format='json')
        self.assertEqual(response.data['events_interested'][0]['id'], str(event.id))

        # Check marking going
        url = '/api/user-me/ues/' + str(event.id) + '?status=2'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 204)
        url = '/api/user-me'
        response = self.client.get(url, format='json')
        self.assertEqual(response.data['events_going'][0]['id'], str(event.id))

        # Check self events
        url = '/api/user-me/events'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], str(event.id))
