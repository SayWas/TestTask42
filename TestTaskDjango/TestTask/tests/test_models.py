from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.test import TestCase

from TestTask.models import Contract, ContractRole

User = get_user_model()


class ModelsTestCase(TestCase):
    fixtures = ['users.json', 'organizations.json',
                'contracts.json']

    def test_contract_clean_method(self):
        contract = Contract.objects.get(pk=1)

        try:
            contract.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")

        contract.title = "Short"
        with self.assertRaises(ValidationError):
            contract.clean()

        contract.title = "Valid Contract Title"
        contract.start_date = timezone.now().date() - timedelta(days=1)
        with self.assertRaises(ValidationError):
            contract.clean()

        contract.start_date = timezone.now().date()
        contract.end_date = timezone.now().date()
        with self.assertRaises(ValidationError):
            contract.clean()

    def test_contract_role_clean_method(self):
        contract = Contract.objects.get(pk=1)
        user = User.objects.get(pk=1)

        contract_role = ContractRole(
            contract=contract,
            user=user,
            role='GD'
        )
        try:
            contract_role.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")

        contract_role.save()
        duplicate_role = ContractRole(
            contract=contract,
            user=user,
            role='GD'
        )
        with self.assertRaises(ValidationError):
            duplicate_role.clean()

        contract_role.role = 'XX'
        with self.assertRaises(ValidationError):
            contract_role.clean()

    def test_contract_role_save_method(self):
        contract = Contract.objects.get(pk=1)
        user = User.objects.get(pk=1)

        contract_role = ContractRole(
            contract=contract,
            user=user,
            role='GD'
        )
        try:
            contract_role.save()
        except ValidationError:
            self.fail("save() raised ValidationError unexpectedly!")
