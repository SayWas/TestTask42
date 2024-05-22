from django.test import TestCase

from TestTask.models import (
    Contract,
    ContractRole,
    User
)
from TestTask.serializers import (
    ContractSerializer,
    ContractRoleSerializer,
    UserSerializer,
    UserContractRoleSerializer
)


class SerializerTestCase(TestCase):
    fixtures = ['users.json', 'organizations.json',
                'contracts.json', 'contract_roles.json']

    def setUp(self):
        self.contract = Contract.objects.get(pk=1)
        self.user = User.objects.get(pk=1)
        self.contract_role = ContractRole.objects.get(pk=1)

    def test_contract_serializer_participants(self):
        serializer = ContractSerializer(self.contract)
        data = serializer.data
        participants = data['participants']

        self.assertEqual(len(participants), 2)

        participant = participants[0]
        self.assertIn('username', participant)
        self.assertIn('full_name', participant)
        self.assertIn('contract_role', participant)
        self.assertIn('organization', participant)

    def test_contract_role_serializer_computed_fields(self):
        serializer = ContractRoleSerializer(self.contract_role)
        data = serializer.data

        self.assertEqual(data['full_name'], self.user.get_full_name())
        self.assertEqual(data['role_display'],
                         self.contract_role.get_role_display())

    def test_user_contract_role_serializer_computed_fields(self):
        serializer = UserContractRoleSerializer(self.contract_role)
        data = serializer.data

        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['full_name'], self.user.get_full_name())
        self.assertEqual(data['contract_role'],
                         self.contract_role.get_role_display())

        organization = data['organization']
        self.assertIsNone(organization)

    def test_user_serializer_computed_fields(self):
        serializer = UserSerializer(self.user)
        data = serializer.data

        self.assertEqual(data['full_name'], self.user.get_full_name())
