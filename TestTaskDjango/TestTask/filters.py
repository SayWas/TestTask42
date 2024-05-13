from django.contrib.contenttypes.models import ContentType
from django.contrib.admin import SimpleListFilter

class OrganizationTypeFilter(SimpleListFilter):
    """
    A custom admin filter based on the type of organization (either Subsidiary or Contractor).
    This filter allows admins to quickly view users associated with a specific type of organization.
    """
    title = 'organization type'
    parameter_name = 'organization_type'

    def lookups(self, request, model_admin):
        return (
            ('subsidiary', 'Subsidiary'),
            ('contractor', 'Contractor'),
        )

    def queryset(self, request, queryset):
        if not hasattr(self, 'content_types'):
            self.content_types = {
                'subsidiary': ContentType.objects.get(model='subsidiary'),
                'contractor': ContentType.objects.get(model='contractor')
            }
        if self.value() in self.content_types:
            return queryset.filter(content_type=self.content_types[self.value()])
        return queryset