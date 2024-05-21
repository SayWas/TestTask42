import csv
from celery import shared_task
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import Contract


@shared_task
def export_to_csv_task(queryset_ids):
    queryset = Contract.objects.filter(id__in=queryset_ids)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contracts.csv"'
    writer = csv.writer(response)
    for obj in queryset:
        writer.writerow([obj.title, obj.status])
    csv_content = response.content.decode('utf-8')

    file_name = 'exports/contracts.csv'
    default_storage.save(file_name, ContentFile(csv_content))

    return file_name
