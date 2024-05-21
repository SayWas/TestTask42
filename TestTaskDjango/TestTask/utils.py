from django.utils.translation import gettext_lazy as _

from .tasks import export_to_csv_task


def export_to_csv(modeladmin, request, queryset):
    """
    Exports a given queryset to a CSV file,
    providing an HTTP response with a download attachment.

    This method is intended to be used as an action within
    Django's admin interface. It writes
    specific fields of each object in the queryset to a CSV file,
    which is then offered as a
    downloadable file to the user.

    Parameters:
    - modeladmin: The ModelAdmin instance defining the action.
    - request: The HttpRequest object.
    - queryset: The QuerySet of the model instances to be exported.

    Returns:
    - HttpResponse: An HTTP response object configured to prompt the user
    to download the CSV file.
    """
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="contracts.csv"'
    # writer = csv.writer(response)
    # for obj in queryset:
    #     writer.writerow([obj.title, obj.status])
    # return response

    queryset_ids = list(queryset.values_list('id', flat=True))
    export_to_csv_task.apply_async(args=[queryset_ids])
    modeladmin.message_user(request, _(
        "The export process has started. When ready selected data will be placed in exports/contracts.csv on server."
    ))


export_to_csv.short_description = _("Export selected to .csv")
