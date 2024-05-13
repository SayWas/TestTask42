from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Subsidiary, Contractor, User, Contract, ContractRole
from .forms import ContractChangeForm, ContractCreationForm, ContractRoleInline, UserChangeAdminForm, UserCreationAdminForm
from .filters import OrganizationTypeFilter
from .utils import export_to_csv

@admin.register(Subsidiary)
class SubsidiaryAdmin(admin.ModelAdmin):
    """
    Admin interface options for Subsidiary model.
    Allows for viewing and editing subsidiaries in the admin interface.
    """
    list_display = ('name', 'is_system_owner')
    list_filter = ('is_system_owner',)
    search_fields = ('name',)

@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    """
    Admin interface options for Contractor model.
    Provides list display, filtering, and search capabilities for contractors.
    """
    list_display = ('name', 'licensed')
    list_filter = ('licensed',)
    search_fields = ('name',)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration to manage User models.
    Extends BaseUserAdmin to include custom fields like job title and organization.
    """
    add_form = UserCreationAdminForm
    form = UserChangeAdminForm
    list_display = ['username','email', 'first_name', 'last_name', 'organization_info', 'job_title']
    list_filter = ('is_active', OrganizationTypeFilter)
    ordering = ('username',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'organization_choice', 'job_title'),
        }),
        ('Permissions', {'fields': ('is_active', 'groups', 'user_permissions')}),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'last_name', 'organization_choice', 'job_title')}),
        ('Permissions', {'fields': ('is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def get_readonly_fields(self, request, obj=None):
        return 'last_login', 'date_joined'

    def get_search_fields(self, request):
        return ['dummy_field']

    def get_search_results(self, request, queryset, search_term):
        base_query = Q()
        if search_term:
            base_query |= Q(username__icontains=search_term) | \
                        Q(first_name__icontains=search_term) | \
                        Q(last_name__icontains=search_term) | \
                        Q(email__icontains=search_term) | \
                        Q(job_title__icontains=search_term)
            content_types = ContentType.objects.get_for_models(Subsidiary, Contractor).values()
            ct_subsidiary = next((ct for ct in content_types if ct.model == 'subsidiary'), None)
            ct_contractor = next((ct for ct in content_types if ct.model == 'contractor'), None)
            org_query = Q(content_type=ct_subsidiary, object_id__in=Subsidiary.objects.filter(name__icontains=search_term).values_list('id', flat=True)) | \
                        Q(content_type=ct_contractor, object_id__in=Contractor.objects.filter(name__icontains=search_term).values_list('id', flat=True))
            if org_query:
                base_query |= org_query
        queryset = queryset.filter(base_query).distinct()
        return queryset, True

    def organization_info(self, obj):
        """ Returns a formatted string of the organization's type and name for display in the admin interface. """
        if obj.organization:
            return "{}: {}".format(obj.organization._meta.model_name.capitalize(), obj.organization.name)
        return _("None")

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """
    Admin configuration to manage Contract models.
    Includes forms for changing and creating contracts, search fields, and custom actions like exporting to CSV.
    """
    form = ContractChangeForm
    add_form = ContractCreationForm
    list_display = ('title', 'organization_do', 'organization_po', 'start_date', 'end_date', 'status', 'contract_details')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('title',)
    actions = [export_to_csv]
    inlines = [ContractRoleInline]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'organization_do', 'organization_po', 'start_date', 'end_date', 'status'),
        }),
    )
    fieldsets = (
        (None, {
            'fields': ('title', 'status')
        }),
        ('Important dates', {
            'fields': ('start_date', 'end_date'),
        }),
        ('Organization Details (After changing all assosiated users will be deleted)', {
            'classes': ('collapse',),
            'fields': ('organization_do', 'organization_po'),
        }),
    )

    def contract_details(self, obj):
        """ Renders HTML format for displaying detailed contract relationships in the admin interface. """
        return format_html(
            "<strong>Between:</strong> {} and {}",
            obj.organization_do, obj.organization_po
        )
    contract_details.short_description = "Contract Details"

    class Media:
        js = ('js/admin_updates.js',)

@admin.register(ContractRole)
class ContractRoleAdmin(admin.ModelAdmin):
    """
    Admin interface to manage ContractRole models.
    Allows listing, filtering, and searching of contract roles linked to users.
    """
    list_display = ('contract', 'user', 'role')
    list_filter = ('role',)
    search_fields = ('contract__title', 'contract__organization_do__name', 'contract__organization_po__name', 'user__username')
