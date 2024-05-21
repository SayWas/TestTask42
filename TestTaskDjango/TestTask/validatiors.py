from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

FirstNameValidator = RegexValidator(
    r'^[A-Za-z\s-]+$',
    _('Enter a valid first name. Only letters, spaces,'
      'and hyphens are allowed.'),
    code='invalid_first_name'
)

LastNameValidator = RegexValidator(
    r'^[A-Za-z\s-]+$',
    _('Enter a valid last name. Only letters, spaces,'
      'and hyphens are allowed.'),
    code='invalid_last_name'
)

OrganizationNameValidator = RegexValidator(
    r'^[A-Za-z\s-]+$',
    _('Enter a valid organization name. Only letters, spaces,'
      'and hyphens are allowed.'),
    code='invalid_organization_name'
)
