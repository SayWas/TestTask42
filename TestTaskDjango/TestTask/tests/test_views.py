import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from TestTask.models import Subsidiary, Contractor, Contract, User, ContractRole
from django.contrib.contenttypes.models import ContentType
from datetime import date

def create_user(username, password, job_title, organization=None):
    user = User.objects.create_user(username=username, password=password, job_title=job_title)
    if organization:
        content_type = ContentType.objects.get_for_model(organization)
        user.content_type = content_type
        user.object_id = organization.id
        user.save()
    return user

def create_contract(title, subsidiary, contractor):
    return Contract.objects.create(
        title=title,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        status="PD",
        organization_do=subsidiary,
        organization_po=contractor
    )

@pytest.mark.django_db
def test_contract_list_view_as_general_director():
    client = APIClient()
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    contractor = Contractor.objects.create(name="Test Contractor")
    
    user = create_user("testuser", "12345", "GD", subsidiary)
    client.force_authenticate(user=user)
    
    create_contract("Test Contract", subsidiary, contractor)
    
    response = client.get(reverse('contract-list'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

@pytest.mark.django_db
def test_contract_list_view_as_non_general_director():
    client = APIClient()
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    contractor = Contractor.objects.create(name="Test Contractor")
    
    user = create_user("testuser", "12345", "MN", subsidiary)
    client.force_authenticate(user=user)
    
    create_contract("Test Contract", subsidiary, contractor)
    
    response = client.get(reverse('contract-list'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0

@pytest.mark.django_db
def test_contract_detail_view():
    client = APIClient()
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    contractor = Contractor.objects.create(name="Test Contractor")
    
    user = create_user("testuser", "12345", "GD", subsidiary)
    client.force_authenticate(user=user)
    
    contract = create_contract("Test Contract", subsidiary, contractor)
    
    response = client.get(reverse('contract-detail', kwargs={'pk': contract.pk}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == "Test Contract"

@pytest.mark.django_db
def test_contract_detail_view_access_restricted():
    client = APIClient()
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    contractor = Contractor.objects.create(name="Test Contractor")
    
    user = create_user("testuser", "12345", "MN", subsidiary)
    client.force_authenticate(user=user)
    
    contract = create_contract("Test Contract", subsidiary, contractor)
    
    response = client.get(reverse('contract-detail', kwargs={'pk': contract.pk}))
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_contract_manage_users_view_get():
    client = APIClient()
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    contractor = Contractor.objects.create(name="Test Contractor")
    
    user = create_user("testuser", "12345", "GD", subsidiary)
    client.force_authenticate(user=user)
    
    contract = create_contract("Test Contract", subsidiary, contractor)
    ContractRole.objects.create(contract=contract, user=user, role="GD")
    
    response = client.get(reverse('contract-manage-users', kwargs={'pk': contract.pk}))
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_contract_manage_users_view_post():
    client = APIClient()
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    contractor = Contractor.objects.create(name="Test Contractor")
    
    user = create_user("testuser", "12345", "GD", subsidiary)
    new_user = create_user("newuser", "12345", "MN", subsidiary)
    client.force_authenticate(user=user)
    
    contract = create_contract("Test Contract", subsidiary, contractor)
    ContractRole.objects.create(contract=contract, user=user, role="GD")
    
    response = client.post(reverse('contract-manage-users', kwargs={'pk': contract.pk}), {'username': 'newuser', 'role': 'MN'})
    assert response.status_code == status.HTTP_201_CREATED
    assert ContractRole.objects.filter(contract=contract, user=new_user, role='MN').exists()

@pytest.mark.django_db
def test_contract_manage_users_view_post_invalid_user():
    client = APIClient()
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    contractor = Contractor.objects.create(name="Test Contractor")
    
    user = create_user("testuser", "12345", "GD", subsidiary)
    client.force_authenticate(user=user)
    
    contract = create_contract("Test Contract", subsidiary, contractor)
    ContractRole.objects.create(contract=contract, user=user, role="GD")
    
    response = client.post(reverse('contract-manage-users', kwargs={'pk': contract.pk}), {'username': 'nonexistentuser', 'role': 'MN'})
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_contract_manage_users_view_delete():
    client = APIClient()
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    contractor = Contractor.objects.create(name="Test Contractor")
    
    user = create_user("testuser", "12345", "GD", subsidiary)
    new_user = create_user("newuser", "12345", "MN", subsidiary)
    client.force_authenticate(user=user)
    
    contract = create_contract("Test Contract", subsidiary, contractor)
    ContractRole.objects.create(contract=contract, user=user, role="GD")
    ContractRole.objects.create(contract=contract, user=new_user, role="MN")
    
    response = client.delete(reverse('contract-manage-users', kwargs={'pk': contract.pk}), {'username': 'newuser', 'role': 'MN'})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not ContractRole.objects.filter(contract=contract, user=new_user, role='MN').exists()

@pytest.mark.django_db
def test_contract_manage_users_view_delete_invalid_user():
    client = APIClient()
    subsidiary = Subsidiary.objects.create(name="Test Subsidiary", is_system_owner=True)
    contractor = Contractor.objects.create(name="Test Contractor")
    
    user = create_user("testuser", "12345", "GD", subsidiary)
    new_user = create_user("newuser", "12345", "MN", subsidiary)
    client.force_authenticate(user=user)
    
    contract = create_contract("Test Contract", subsidiary, contractor)
    ContractRole.objects.create(contract=contract, user=user, role="GD")
    ContractRole.objects.create(contract=contract, user=new_user, role="MN")
    
    response = client.delete(reverse('contract-manage-users', kwargs={'pk': contract.pk}), {'username': 'nonexistentuser', 'role': 'MN'})
    assert response.status_code == status.HTTP_404_NOT_FOUND
