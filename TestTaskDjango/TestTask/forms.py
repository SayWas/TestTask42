import re
from itertools import chain

from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.forms import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Contract, ContractRole, Contractor, Subsidiary, User
from .validatiors import FirstNameValidator, LastNameValidator


class ContractRoleInline(admin.TabularInline):
    """
    Defines inline placement of ContractRole in the admin form,
    allowing easy editing of related roles directly from the contract form.
    """
    model = ContractRole
    extra = 1


class BaseUserForm(forms.ModelForm):
    """
    Base form for user creation and editing. This form adds custom fields
    for selecting organizations and setting job titles.
    """
    organization_choice = forms.ChoiceField(
        label=_('Organization'),
        help_text="Changing organization will cause all associated contracts\
            to be removed."
    )
    first_name = forms.CharField(
        validators=[FirstNameValidator]
    )
    last_name = forms.CharField(
        validators=[LastNameValidator]
    )
    job_title = forms.ChoiceField(
        choices=User.JOB_TITLE_CHOICES,
        label=_('Job Title')
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'organization_choice', 'job_title', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization_choice'].choices = [
            ('', '---------')] + self.get_organization_choices()
        if self.instance.pk and self.instance.organization:
            self.fields['organization_choice'].initial = (
                f"{self.instance.content_type.model}_{self.instance.object_id}"
            )

    def get_organization_choices(self):
        """
        Retrieves a combined list of all subsidiaries and contractors
        to populate the organization_choice field.
        """
        organizations = chain(Subsidiary.objects.all(),
                              Contractor.objects.all())
        return [
            (
                f'{org._meta.model_name}_{org.pk}',
                f'{org._meta.verbose_name.title()}: {org.name}'
            )
            for org in organizations]

    def save(self, commit=True):
        instance = super().save(commit=False)
        org_choice = self.cleaned_data['organization_choice']
        if org_choice:
            model_name, id = org_choice.split('_')
            model_class = (Subsidiary if model_name == 'subsidiary'
                           else Contractor)
            instance.content_type = ContentType.objects.get_for_model(
                model_class)
            instance.object_id = int(id)
        else:
            instance.content_type = None
            instance.object_id = None
        if commit:
            instance.save()
        return instance


class UserChangeAdminForm(BaseUserForm, UserChangeForm):
    """
    Form for changing existing users. Inherits from BaseUserForm
    and Django's UserChangeForm.
    """
    pass


class UserCreationAdminForm(BaseUserForm, UserCreationForm):
    """
    Form for creating new users. Inherits from BaseUserForm
    and Django's UserCreationForm.
    """
    pass


class BaseContractForm(forms.ModelForm):
    """
    Base form for contract operations. Includes common validations
    shared across creation and change forms.
    """
    class Meta:
        model = Contract
        exclude = ['contract_details']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title and not re.match(r'^[A-Za-z0-9 \-]{10,100}$', title):
            self.add_error('title', _(
                'The title must be between 10 and 100 characters long and can '
                'only contain letters, numbers, spaces, and hyphens.'
            ))
        return cleaned_data


class ContractCreationForm(BaseContractForm):
    """
    Base form for contract operations. Includes common validations
    shared across creation and change forms.
    """

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and start_date < timezone.now().date():
            self.add_error('start_date', _(
                'The start date cannot be in the past.'))
        if start_date and end_date and start_date >= end_date:
            self.add_error('end_date', _(
                'The end date must be after the start date.'))
        return cleaned_data


class ContractChangeForm(BaseContractForm):
    """
    Form for changing existing contracts. Manages additional logic
    related to related entities, such as contract roles.
    """

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit and instance:
            instance.save()
            self.save_m2m()
            self.handle_contract_roles(instance)
        return instance

    def handle_contract_roles(self, contract):
        """
        Ensures that contract roles are updated based
        on the current organizations participating in the contract.
        """
        try:
            if contract.organization_do_id and contract.organization_po_id:
                with transaction.atomic():
                    valid_companies = {
                        contract.organization_do_id,
                        contract.organization_po_id
                    }
                    ContractRole.objects.filter(contract=contract).exclude(
                        user__object_id__in=valid_companies).delete()
        except Exception:
            raise ValidationError(
                _('An error occurred while updating contract roles.'),
                code='invalid'
            )
