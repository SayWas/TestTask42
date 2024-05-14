import pytest
from django.contrib.contenttypes.models import ContentType
from TestTask.serializers import (
    SubsidiarySerializer,
    ContractorSerializer,
    ContractSerializer,
    ContractRoleSerializer,
    UserSerializer,
    UserContractRoleSerializer
)
from TestTask.models import Subsidiary, Contractor, Contract, ContractRole, User
from datetime import date

@pytest.mark.django_db
def test_subsidiary_serializer():
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    serializer = SubsidiarySerializer(subsidiary)
    data = serializer.data
    assert data['name'] == "Test Subsidiary"
    assert data['is_system_owner'] == True

@pytest.mark.django_db
def test_contractor_serializer():
    contractor = Contractor.objects.create(name="Test Contractor", licensed=True)
    serializer = ContractorSerializer(contractor)
    data = serializer.data
    assert data['name'] == "Test Contractor"
    assert data['licensed'] == True

@pytest.mark.django_db
def test_user_serializer():
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    content_type = ContentType.objects.get_for_model(Subsidiary)
    user = User.objects.create_user(
        username="testuser",
        password="12345",
        first_name="Test",
        last_name="User",
        content_type=content_type,
        object_id=subsidiary.id,
        job_title="GD"
    )
    serializer = UserSerializer(user)
    data = serializer.data
    assert data['username'] == "testuser"
    assert data['full_name'] == "Test User"

@pytest.mark.django_db
def test_contract_serializer():
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
    serializer = ContractSerializer(contract)
    data = serializer.data
    assert data['title'] == "Test Contract"
    assert data['status'] == "PD"
    assert data['organization_do']['name'] == "Test Subsidiary"
    assert data['organization_po']['name'] == "Test Contractor"
    assert 'participants' in data

@pytest.mark.django_db
def test_contract_role_serializer():
    user = User.objects.create_user(username="testuser", password="12345", first_name="Test", last_name="User")
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
    serializer = ContractRoleSerializer(role)
    data = serializer.data
    assert data['full_name'] == "Test User"
    assert data['role_display'] == "Manager"

@pytest.mark.django_db
def test_user_contract_role_serializer():
    user = User.objects.create_user(username="testuser", password="12345", first_name="Test", last_name="User")
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    content_type = ContentType.objects.get_for_model(Subsidiary)
    user.content_type = content_type
    user.object_id = subsidiary.id
    user.save()
    
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
    serializer = UserContractRoleSerializer(role)
    data = serializer.data
    assert data['username'] == "testuser"
    assert data['full_name'] == "Test User"
    assert data['contract_role'] == "Manager"
    assert data['organization']['name'] == "Test Subsidiary"
    assert data['organization']['is_system_owner'] == True
