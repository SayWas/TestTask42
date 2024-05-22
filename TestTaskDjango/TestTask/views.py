from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from rest_framework import permissions, status, views

from .mixins import ContractPermissionMixin
from .models import Contract, ContractRole, Contractor, Subsidiary, User
from .permissions import (
    IsContractGeneralDirectorOrGeneralDirector,
    IsGeneralDirectorOrRelatedUser
)
from .serializers import ContractSerializer, UserSerializer
from .responses import CustomResponse, CustomNotFound


class ContractListView(views.APIView):
    """
    API view to list all contracts for an authenticated user based
    on their role and associated organization.
    General Directors can view all contracts, while other users can only see
    contracts linked to their organization.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_is_general_director = user.job_title == 'GD'

        if user_is_general_director:
            if (hasattr(user.organization, 'is_system_owner') and
                    user.organization.is_system_owner):
                contracts = Contract.objects.all()
            else:
                contracts = Contract.objects.filter(roles__user=user)
                if isinstance(user.organization, Subsidiary):
                    contracts |= Contract.objects.filter(
                        organization_do=user.organization)
                elif isinstance(user.organization, Contractor):
                    contracts |= Contract.objects.filter(
                        organization_po=user.organization)
        else:
            contracts = Contract.objects.filter(roles__user=user)

        contracts = contracts.distinct()
        serializer = ContractSerializer(contracts, many=True)
        return CustomResponse(serializer.data)


class ContractDetailView(views.APIView, ContractPermissionMixin):
    """
    API view to retrieve a detailed view of a single contract.
    Access is controlled by user permissions.
    Users need to be a General Director or related to
    the contract through their organization.
    """
    permission_classes = [permissions.IsAuthenticated,
                          IsGeneralDirectorOrRelatedUser]

    def get(self, request, pk):
        contract = self.get_contract(pk)
        if not contract:
            raise CustomNotFound()
        serializer = ContractSerializer(contract)
        return CustomResponse(serializer.data)


class ContractManageUsersView(views.APIView, ContractPermissionMixin):
    """
    API view to manage users associated with a specific contract.
    Allows adding and removing users from contracts, restricted to users
    with appropriate permissions.
    """
    permission_classes = [permissions.IsAuthenticated,
                          IsContractGeneralDirectorOrGeneralDirector]

    def get(self, request, pk):
        contract = self.get_contract(pk)
        if not contract:
            raise CustomNotFound()
        user = request.user

        if self.check_general_director_permissions(user):
            return CustomResponse(
                UserSerializer(User.objects.all(), many=True).data
            )
        if not contract.roles.filter(user=user, role='GD').exists():
            return CustomResponse({'detail': _(
                'You do not have permission to manage this contract.')
            }, status=status.HTTP_403_FORBIDDEN)

        eligible_users = User.objects.filter(
            Q(content_type=ContentType.objects.get_for_model(Subsidiary),
              object_id=contract.organization_do_id) |
            Q(content_type=ContentType.objects.get_for_model(
                Contractor), object_id=contract.organization_po_id)
        ).distinct()

        serializer = UserSerializer(eligible_users, many=True)
        return CustomResponse(serializer.data)

    def post(self, request, pk):
        contract = self.get_contract(pk)
        if not contract:
            raise CustomNotFound()
        user = request.user
        if (not self.check_general_director_permissions(user) and
                not contract.roles.filter(user=user, role='GD').exists()):
            return CustomResponse({'detail': _(
                'You do not have permission to manage this contract.')},
                status=status.HTTP_403_FORBIDDEN)

        try:
            new_user = User.objects.get(username=request.data.get('username'))
        except User.DoesNotExist:
            raise CustomNotFound()

        if (not (new_user.organization == contract.organization_do or
                 new_user.organization == contract.organization_po) and
                not self.check_general_director_permissions(user)):
            return CustomResponse({'detail': _(
                'User must be a member of an organization '
                'part of this contract.')
            }, status=status.HTTP_403_FORBIDDEN)
        contract_role = request.data.get('role')
        if (contract_role and
                contract_role not in ['GD', 'VD', 'MN', 'SP', 'AS']):
            return CustomResponse({'detail': _(
                'Invalid data passed.')},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            ContractRole.objects.create(
                contract=contract, user=new_user, role=contract_role)
        except:
            return CustomResponse({'detail': _(
                'Invalid data passed.')},
                status=status.HTTP_400_BAD_REQUEST)
        return CustomResponse({'detail': _(
            'User added successfully.')},
            status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = request.user
        contract = self.get_contract(pk)
        if not contract:
            raise CustomNotFound()
        if (not self.check_general_director_permissions(user) and
                not contract.roles.filter(user=user, role='GD').exists()):
            return CustomResponse({'detail': _(
                'You do not have permission to manage this contract.')},
                status=status.HTTP_403_FORBIDDEN)

        contract_role = request.data.get('role')
        if (contract_role and
                contract_role not in ['GD', 'VD', 'MN', 'SP', 'AS']):
            return CustomResponse({'detail': _(
                'Invalid data passed.')},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            user_to_delete = User.objects.get(
                username=request.data.get('username'))
        except User.DoesNotExist:
            raise CustomNotFound()

        try:
            role_to_delete = ContractRole.objects.get(
                contract=contract,
                user=user_to_delete,
                role=contract_role
            )
        except ContractRole.DoesNotExist:
            raise CustomNotFound()

        role_to_delete.delete()
        return CustomResponse({'detail': _(
            'User removed successfully.')},
            status=status.HTTP_204_NO_CONTENT)


@login_required
def fetch_users(request):
    """
    Function-based view to fetch users based on organization IDs.
    Validates that the IDs provided are integers and
    responds with user details if valid.
    """
    org_do_id = request.GET.get('org_do_id')
    org_po_id = request.GET.get('org_po_id')
    if not org_do_id or not org_po_id:
        return JsonResponse(
            {'error': 'Both org_do_id and org_po_id must be provided and not empty.'},
            status=status.HTTP_400_BAD_REQUEST)
    try:
        org_do_id = int(org_do_id)
        org_po_id = int(org_po_id)
    except ValueError:
        return JsonResponse(
            {'error': 'org_do_id and org_po_id must be valid integers.'},
            status=status.HTTP_400_BAD_REQUEST)
    users = User.objects.filter(
        content_type__in=[ContentType.objects.get_for_model(
            Subsidiary), ContentType.objects.get_for_model(Contractor)],
        object_id__in=[org_do_id, org_po_id]
    ).distinct()
    user_data = [{'id': user.id, 'text': user.username} for user in users]
    return JsonResponse(user_data, safe=False)
