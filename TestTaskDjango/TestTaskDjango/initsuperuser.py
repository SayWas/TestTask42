from environ import Env
from django.contrib.auth import get_user_model

User = get_user_model()

env = Env()
env.read_env()
username = env("DJANGO_SUPERUSER_USERNAME", default="admin")
email = env("DJANGO_SUPERUSER_EMAIL", default="admin@example.com")
password = env("DJANGO_SUPERUSER_PASSWORD", default="admin")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created.')
else:
    print('Superuser creation skipped.')