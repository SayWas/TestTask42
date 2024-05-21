from decouple import config
from django.contrib.auth import get_user_model

User = get_user_model()

username = config('DJANGO_SUPERUSER_USERNAME', default='admin')
email = config('DJANGO_SUPERUSER_EMAIL', default='admin@example.com')
password = config('DJANGO_SUPERUSER_PASSWORD', default='admin')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created.')
else:
    print('Superuser creation skipped.')
