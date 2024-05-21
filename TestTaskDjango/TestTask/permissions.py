from rest_framework.permissions import BasePermission

from .models import Contractor, Subsidiary


class IsGeneralDirectorOrRelatedUser(BasePermission):
    """Allow access to GDs of system-owner organizations or related users."""

    def has_permission(self, request, view):
        user = request.user
        user_is_general_director = user.job_title == 'GD'
        contract = view.get_contract(view.kwargs['pk'])

        if user_is_general_director:
            if (hasattr(user.organization, 'is_system_owner') and
                    user.organization.is_system_owner):
                return True
            if (isinstance(user.organization, Subsidiary) and
                    contract.organization_do == user.organization):
                return True
            elif (isinstance(user.organization, Contractor) and
                    contract.organization_po == user.organization):
                return True
        return contract.roles.filter(user=user).exists()


class IsContractGeneralDirectorOrGeneralDirector(BasePermission):
    """
    Allows access only to general directors of the contract or general director
    of system owning company.
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            user.job_title == 'GD'
            and hasattr(user.organization, 'is_system_owner')
            and user.organization.is_system_owner
        ) or (
            view.get_contract(view.kwargs.get('pk')).roles.filter(
                user=user, role='GD').exists()
        )
