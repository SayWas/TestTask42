from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.test import TestCase

from TestTask.models import Subsidiary, Contractor, Contract, ContractRole

User = get_user_model()


class ModelsTestCase(TestCase):
    fixtures = ['users.json', 'organizations.json', 'contracts.json']

    def test_create_subsidiary(self):
        Subsidiary.objects.create(name="New Subsidiary", is_system_owner=False)
        new_subsidiary = Subsidiary.objects.get(name="New Subsidiary")
        self.assertEqual(Subsidiary.objects.count(), 2)
        self.assertFalse(new_subsidiary.is_system_owner)

    def test_create_contractor(self):
        Contractor.objects.create(name="New Contractor", licensed=False)
        new_contractor = Contractor.objects.get(name="New Contractor")
        self.assertEqual(Contractor.objects.count(), 2)
        self.assertFalse(new_contractor.licensed)

    def test_create_user(self):
        content_type = ContentType.objects.get_for_model(Subsidiary)
        User.objects.create_user(
            username="newuser",
            password="12345",
            first_name="Test",
            last_name="User",
            content_type=content_type,
            object_id=Subsidiary.objects.get(pk=1).id,
            job_title="GD"
        )
        new_user = User.objects.get(username="newuser")
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(new_user.username, "newuser")

    def test_create_contract(self):
        subsidiary = Subsidiary.objects.get(pk=1)
        contractor = Contractor.objects.get(pk=2)
        contract = Contract.objects.create(
            title="Another Test Contract",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            status="PD",
            organization_do=subsidiary,
            organization_po=contractor
        )
        self.assertEqual(contract.title, "Another Test Contract")
        self.assertEqual(contract.status, "PD")
        self.assertEqual(contract.organization_do, subsidiary)
        self.assertEqual(contract.organization_po, contractor)

    def test_create_contract_role(self):
        user = User.objects.get(pk=1)
        contract = Contract.objects.get(pk=1)
        role = ContractRole.objects.create(
            contract=contract, user=user, role="MN")
        self.assertEqual(role.role, "MN")
        self.assertEqual(role.contract, contract)
        self.assertEqual(role.user, user)

    def test_contract_clean_method(self):
        subsidiary = Subsidiary.objects.get(pk=1)
        contractor = Contractor.objects.get(pk=2)
        contract = Contract(
            title="Invalid",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            status="PD",
            organization_do=subsidiary,
            organization_po=contractor
        )
        with self.assertRaises(ValidationError):
            contract.clean()

        contract.title = "Valid Title"
        contract.start_date = date(2023, 1, 1)
        with self.assertRaises(ValidationError):
            contract.clean()

        contract.start_date = date(2024, 12, 31)
        contract.end_date = date(2024, 1, 1)
        with self.assertRaises(ValidationError):
            contract.clean()

    def test_contract_role_unique(self):
        user = User.objects.get(pk=1)
        contract = Contract.objects.get(pk=1)
        ContractRole.objects.create(contract=contract, user=user, role="MN")
        with self.assertRaises(ValidationError):
            duplicate_role = ContractRole(
                contract=contract, user=user, role="MN")
            duplicate_role.clean()

    def test_delete_contract_deletes_roles(self):
        contract = Contract.objects.get(pk=1)
        user = User.objects.get(pk=1)
        ContractRole.objects.create(contract=contract, user=user, role="MN")
        contract.delete()
        self.assertEqual(Contract.objects.count(), 0)
        self.assertEqual(ContractRole.objects.count(), 0)
