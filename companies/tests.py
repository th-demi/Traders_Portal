from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Company

# Create your tests here.

class CompanyAPITests(APITestCase):
    def setUp(self):
        Company.objects.create(company_name='Test Company', symbol='TST', scripcode='123')
        Company.objects.create(company_name='Another Company', symbol='ANC', scripcode='456')

    def test_list_companies(self):
        url = reverse('company-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_search_company_by_name(self):
        url = reverse('company-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any('Test Company' in c['company_name'] for c in response.data))

    def test_filter_company_by_symbol(self):
        url = reverse('company-list')
        response = self.client.get(url, {'symbol': 'TST'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(c['symbol'] == 'TST' for c in response.data))
