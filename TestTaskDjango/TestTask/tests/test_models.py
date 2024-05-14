import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from TestTask.models import Subsidiary, Contractor, Contract, ContractRole
from datetime import date

User = get_user_model()

@pytest.mark.django_db
def test_create_subsidiary():
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    assert Subsidiary.objects.count() == 1
    assert subsidiary.name == "Test Subsidiary"
    assert subsidiary.is_system_owner

@pytest.mark.django_db
def test_create_contractor():
    contractor = Contractor.objects.create(name="Test Contractor", licensed=True)
    assert Contractor.objects.count() == 1
    assert contractor.name == "Test Contractor"
    assert contractor.licensed

@pytest.mark.django_db
def test_create_user():
    content_type = ContentType.objects.get_for_model(Subsidiary)
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    user = User.objects.create_user(
        username="testuser",
        password="12345",
        first_name="Test",
        last_name="User",
        content_type=content_type,
        object_id=subsidiary.id,
        job_title="GD"
    )
    assert User.objects.count() == 1
    assert user.username == "testuser"
    assert user.organization == subsidiary
    assert user.job_title == "GD"

@pytest.mark.django_db
def test_create_contract():
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary")
    contractor = Contractor.objects.create(name="Test Contractor")
    contract = Contract.objects.create(
        title="Test Contract",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        status="PD",
        organization_do=subsidiary,
        organization_po=contractor
    )
    assert Contract.objects.count() == 1
    assert contract.title == "Test Contract"
    assert contract.status == "PD"
    assert contract.organization_do == subsidiary
    assert contract.organization_po == contractor

@pytest.mark.django_db
def test_create_contract_role():
    user = User.objects.create_user(username="testuser", password="12345")
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary")
    contractor = Contractor.objects.create(name="Test Contractor")
    contract = Contract.objects.create(
        title="Test Contract",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        status="PD",
        organization_do=subsidiary,
        organization_po=contractor
    )
    role = ContractRole.objects.create(contract=contract, user=user, role="MN")
    assert ContractRole.objects.count() == 1
    assert role.role == "MN"
    assert role.contract == contract
    assert role.user == user

@pytest.mark.django_db
def test_contract_clean_method():
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary")
    contractor = Contractor.objects.create(name="Test Contractor")

    contract = Contract(
        title="Invalid",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        status="PD",
        organization_do=subsidiary,
        organization_po=contractor
    )
    with pytest.raises(ValidationError) as excinfo:
        contract.clean()
    assert 'The title must be between 10 and 100 characters long and can only contain letters, numbers, spaces, and hyphens.' in str(excinfo.value)

    contract.title = "Valid Title"
    contract.start_date = date(2023, 1, 1)
    with pytest.raises(ValidationError) as excinfo:
        contract.clean()
    assert 'The start date cannot be earlier than today.' in str(excinfo.value)

    contract.start_date = date(2024, 12, 31)
    contract.end_date = date(2024, 1, 1)
    with pytest.raises(ValidationError) as excinfo:
        contract.clean()
    assert 'The start date cannot be after or equal to the end date.' in str(excinfo.value)

@pytest.mark.django_db
def test_contract_role_unique():
    user = User.objects.create_user(username="testuser", password="12345")
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary")
    contractor = Contractor.objects.create(name="Test Contractor")
    contract = Contract.objects.create(
        title="Test Contract",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        status="PD",
        organization_do=subsidiary,
        organization_po=contractor
    )
    ContractRole.objects.create(contract=contract, user=user, role="MN")
    
    with pytest.raises(ValidationError) as excinfo:
        duplicate_role = ContractRole(contract=contract, user=user, role="MN")
        duplicate_role.clean()
    assert 'This user is already assigned this role in this contract.' in str(excinfo.value)

@pytest.mark.django_db
def test_str_methods():
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary")
    contractor = Contractor.objects.create(name="Test Contractor")
    user = User.objects.create_user(username="testuser", password="12345", first_name="Test", last_name="User")
    
    contract = Contract.objects.create(
        title="Test Contract",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        status="PD",
        organization_do=subsidiary,
        organization_po=contractor
    )
    
    role = ContractRole.objects.create(contract=contract, user=user, role="MN")
    
    assert str(subsidiary) == "Test Subsidiary"
    assert str(contractor) == "Test Contractor"
    assert str(contract) == "Test Contract between Test Subsidiary and Test Contractor"
    assert str(role) == "Test User as Manager in Test Contract"

@pytest.mark.django_db
def test_delete_contract_deletes_roles():
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary")
    contractor = Contractor.objects.create(name="Test Contractor")
    user = User.objects.create_user(username="testuser", password="12345")
    
    contract = Contract.objects.create(
        title="Test Contract",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        status="PD",
        organization_do=subsidiary,
        organization_po=contractor
    )
    
    role = ContractRole.objects.create(contract=contract, user=user, role="MN")
    contract.delete()
    
    assert Contract.objects.count() == 0
    assert ContractRole.objects.count() == 0
