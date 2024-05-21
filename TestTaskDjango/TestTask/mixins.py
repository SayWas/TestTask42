from django.http import Http404
from django.utils.translation import gettext_lazy as _

from .models import Contract


class ContractPermissionMixin:
    """
    A mixin class that provides permission checks and utility methods for
    handling contracts. Specifically, it helps in determining if a user has
    general director permissions for a specific contract.
    """

    def check_general_director_permissions(self, user):
        """
        Check if the user is a GD with the right to view
        or manage the contract.
        """
        return (
            user.job_title == 'GD' and
            hasattr(user.organization, 'is_system_owner') and
            user.organization.is_system_owner
        )

    def get_contract(self, pk):
        """
        Retrieve contract with error handling.
        """
        try:
            return Contract.objects.get(pk=pk)
        except Contract.DoesNotExist:
            raise Http404(_("Contract does not exist"))
