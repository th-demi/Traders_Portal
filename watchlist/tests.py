from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Watchlist
from companies.models import Company
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class WatchlistAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='watchuser', password='Testpass123!')
        self.company = Company.objects.create(company_name='Watch Co', symbol='WTC', scripcode='789')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_add_to_watchlist(self):
        url = reverse('watchlist-list')
        data = {'company_id': self.company.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Watchlist.objects.filter(user=self.user, company=self.company).exists())

    def test_list_watchlist(self):
        Watchlist.objects.create(user=self.user, company=self.company)
        url = reverse('watchlist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(w['company']['company_name'] == 'Watch Co' for w in response.data))

    def test_remove_from_watchlist(self):
        watch = Watchlist.objects.create(user=self.user, company=self.company)
        url = reverse('watchlist-detail', args=[watch.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Watchlist.objects.filter(id=watch.id).exists())
