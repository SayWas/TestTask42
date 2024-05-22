from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from TestTask.models import Contract

User = get_user_model()


class ContractViewTests(APITestCase):
    fixtures = [
        'users.json', 'organizations.json',
        'contracts.json', 'contract_roles.json'
    ]

    def setUp(self):
        self.client = APIClient()

        self.general_director = User.objects.get(username='testuser')
        self.non_general_director = User.objects.get(username='testuser2')

        self.general_director.set_password('password')
        self.general_director.save()
        self.non_general_director.set_password('password')
        self.non_general_director.save()

        self.general_director_token = str(
            RefreshToken.for_user(self.general_director).access_token)
        self.non_general_director_token = str(
            RefreshToken.for_user(self.non_general_director).access_token)

        self.contract = Contract.objects.get(pk=1)

    def test_contract_list_view_as_general_director(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {
                                self.general_director_token}')
        response = self.client.get(reverse('contract-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_contract_list_view_as_non_general_director(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {
                                self.non_general_director_token}')
        response = self.client.get(reverse('contract-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_contract_detail_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {
                                self.general_director_token}')
        response = self.client.get(
            reverse('contract-detail', kwargs={'pk': self.contract.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['title'], "Test Contract")

    def test_contract_manage_users_view_get(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {
                                self.general_director_token}')
        response = self.client.get(
            reverse('contract-manage-users', kwargs={'pk': self.contract.pk}))
        self.assertEqual(response.status_code, 200)

    def test_contract_manage_users_view_post_invalid_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {
                                self.general_director_token}')
        response = self.client.post(
            reverse('contract-manage-users', kwargs={'pk': self.contract.pk}),
            {'username': 'nonexistentuser', 'role': 'MN'})
        self.assertEqual(response.status_code, 404)

    def test_fetch_users(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('fetch_users'), {
                                   'org_do_id': 1, 'org_po_id': 2})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
