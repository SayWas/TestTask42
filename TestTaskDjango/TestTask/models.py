import re

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .validatiors import (
    FirstNameValidator,
    LastNameValidator,
    OrganizationNameValidator
)


class Organization(models.Model):
    """
    Abstract base model for an organization with a name.
    """
    name = models.CharField(max_length=255, validators=[
                            OrganizationNameValidator])

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ['name']

    def __str__(self):
        return self.name


class Subsidiary(Organization):
    """
    Model representing a subsidiary which is a specific type of organization.
    """
    is_system_owner = models.BooleanField(default=False)


class Contractor(Organization):
    """
    Model representing a contractor which is a specific type of organization
    and has a license status.
    """
    licensed = models.BooleanField(default=False)


class User(AbstractUser):
    """
    User model extending Django's AbstractUser to include job title
    and association with an organization.
    """
    JOB_TITLE_CHOICES = (
        ('GD', _('General Director')),
        ('VD', _('Vice Director')),
        ('MN', _('Manager')),
        ('SP', _('Specialist')),
        ('AS', _('Assistant')),
    )
    first_name = models.CharField(
        max_length=255, validators=[FirstNameValidator])
    last_name = models.CharField(
        max_length=255, validators=[LastNameValidator])
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(app_label='TestTask', model='subsidiary') |
        models.Q(app_label='TestTask', model='contractor'),
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    organization = GenericForeignKey('content_type', 'object_id')
    job_title = models.CharField(max_length=255, choices=JOB_TITLE_CHOICES)


class Contract(models.Model):
    """
    Model representing a contract between organizations,
    with start and end dates, and a status.
    """
    STATUS_CHOICES = (
        ('PD', _('Paid')),
        ('UP', _('Unpaid')),
    )
    title = models.CharField(max_length=100)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='OP')
    organization_do = models.ForeignKey(
        Subsidiary, on_delete=models.CASCADE, related_name='contracts_do')
    organization_po = models.ForeignKey(
        Contractor, on_delete=models.CASCADE, related_name='contracts_po')

    def clean(self):
        """
        Validates that the contract has valid title, dates, and logical
        start/end date arrangement.
        """
        if not self.title or not re.match(
            r'^[A-Za-z0-9 \-]{10,100}$',
                self.title):
            raise ValidationError(
                _('The title must be between 10 and 100 characters long and'
                  'can only contain letters, numbers, spaces, and hyphens.'),
                code='invalid_title'
            )
        if self._state.adding and self.start_date < timezone.now().date():
            raise ValidationError(
                _('The start date cannot be earlier than today.'),
                code='start_date_past'
            )
        if self.start_date >= self.end_date:
            raise ValidationError(
                _('The start date cannot be after or equal to the end date.'),
                code='start_date_after_end_date'
            )

    def __str__(self):
        return _("{title} between {organization_do} and {organization_po}"
                 ).format(title=self.title,
                          organization_do=self.organization_do,
                          organization_po=self.organization_po)


class ContractRole(models.Model):
    """
    Model linking users to contracts with specific roles.
    """
    ROLE_CHOICES = (
        ('GD', _('General Director')),
        ('VD', _('Vice Director')),
        ('MN', _('Manager')),
        ('SP', _('Specialist')),
        ('AS', _('Assistant')),
    )
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="roles")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contract_roles")
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)

    def clean(self):
        if ContractRole.objects.filter(
            contract=self.contract,
            user=self.user,
            role=self.role
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                _("This user is already assigned this role in this contract.")
            )

        valid_roles = [choice[0] for choice in self.ROLE_CHOICES]
        if self.role not in valid_roles:
            raise ValidationError(_("Invalid role selected."))

    def save(self, *args, **kwargs):
        self.clean()
        super(ContractRole, self).save(*args, **kwargs)

    def __str__(self):
        return _("{full_name} as {role} in {title}").format(
            full_name=self.user.get_full_name(),
            role=self.get_role_display(),
            title=self.contract.title
        )
