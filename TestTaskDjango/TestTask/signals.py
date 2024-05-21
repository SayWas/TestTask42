from django.db import transaction
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Contract, ContractRole, User


def get_user_contracts(user):
    """
    Retrieves a set of contract IDs associated with a given
    user through contract roles.

    Parameters:
    - user (User): The user instance whose contracts are to be retrieved.

    Returns:
    - set: A set of contract IDs.
    """
    return set(ContractRole.objects.filter(user=user)
               .values_list('contract_id', flat=True))


def get_invalid_contract_ids(user_id, valid_contract_ids):
    """
    Filters out contract IDs that are no longer valid for a user based
    on changes in associated organizations.

    Parameters:
    - user_id (int): The ID of the user's current organization.
    - valid_contract_ids (set): A set of contract IDs currently
    linked to the user.

    Returns:
    - set: A set of contract IDs that are no longer valid.
    """
    return set(
        Contract.objects.filter(
            ~Q(organization_do_id=user_id) & ~Q(organization_po_id=user_id),
            id__in=valid_contract_ids
        ).values_list('id', flat=True)
    )


@receiver(pre_save, sender=User)
def update_user_contract_roles(sender, instance, **kwargs):
    """
    Signal to update the contract roles for a user before saving,
    if there are changes in the user's associated organization.
    This ensures that the user is only linked to contracts that involve
    the organization they are currently part of.

    Parameters:
    - sender (Model class): The model class that sent the signal.
    - instance (User): The instance of the model that's about to be saved.
    - kwargs (dict): Additional keyword arguments.
    """
    if instance.pk:
        try:
            old_user = User.objects.only(
                'object_id', 'content_type').get(pk=instance.pk)
            if (old_user.object_id != instance.object_id or
                    old_user.content_type != instance.content_type):
                with transaction.atomic():
                    current_contracts_ids = get_user_contracts(instance)
                    non_valid_contracts_ids = get_invalid_contract_ids(
                        instance.object_id, current_contracts_ids
                    )
                    ContractRole.objects.filter(
                        user=instance, contract_id__in=non_valid_contracts_ids
                    ).delete()
        except User.DoesNotExist:
            pass
