from django.test import TestCase

from TestTask.models import (
    Subsidiary,
    Contractor,
    Contract,
    ContractRole,
    User
)
from TestTask.serializers import (
    SubsidiarySerializer,
    ContractorSerializer,
    ContractSerializer,
    ContractRoleSerializer,
    UserSerializer,
    UserContractRoleSerializer
)


class SerializerTestCase(TestCase):
    fixtures = ['users.json', 'organizations.json',
                'contracts.json', 'contract_roles.json']

    def test_subsidiary_serializer(self):
        subsidiary = Subsidiary.objects.get(pk=1)
        serializer = SubsidiarySerializer(subsidiary)
        self.assertEqual(serializer.data['name'], "Test Subsidiary")
        self.assertTrue(serializer.data['is_system_owner'])

    def test_contractor_serializer(self):
        contractor = Contractor.objects.get(pk=2)
        serializer = ContractorSerializer(contractor)
        self.assertEqual(serializer.data['name'], "Test Contractor")
        self.assertTrue(serializer.data['licensed'])

    def test_user_serializer(self):
        user = User.objects.get(username="testuser")
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data['username'], "testuser")
        self.assertEqual(serializer.data['full_name'], "Test User")

    def test_contract_serializer(self):
        contract = Contract.objects.get(pk=1)
        serializer = ContractSerializer(contract)
        self.assertEqual(serializer.data['title'], "Test Contract")
        self.assertEqual(serializer.data['status'], "PD")
        self.assertEqual(
            serializer.data['organization_do']['name'], "Test Subsidiary")
        self.assertEqual(
            serializer.data['organization_po']['name'], "Test Contractor")
        self.assertIn('participants', serializer.data)

    def test_contract_role_serializer(self):
        role = ContractRole.objects.get(pk=1)
        serializer = ContractRoleSerializer(role)
        self.assertEqual(serializer.data['full_name'], "Test User")
        self.assertEqual(serializer.data['role_display'], "General Director")

    def test_user_contract_role_serializer(self):
        role = ContractRole.objects.get(pk=1)
        serializer = UserContractRoleSerializer(role)
        self.assertEqual(serializer.data['username'], "testuser")
        self.assertEqual(serializer.data['full_name'], "Test User")
        self.assertEqual(serializer.data['contract_role'], "General Director")
