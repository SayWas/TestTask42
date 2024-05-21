# Generated by Django 4.2.11 on 2024-05-13 13:54

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('PD', 'Paid'), ('UP', 'Unpaid')], default='OP', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[A-Za-z\\s-]+$', 'Enter a valid organization name. Only letters, spaces, and hyphens are allowed.', code='invalid_organization_name')])),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('organization_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TestTask.organization')),
                ('licensed', models.BooleanField(default=False)),
            ],
            bases=('TestTask.organization',),
        ),
        migrations.CreateModel(
            name='Subsidiary',
            fields=[
                ('organization_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TestTask.organization')),
                ('is_system_owner', models.BooleanField(default=False)),
            ],
            bases=('TestTask.organization',),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[A-Za-z\\s-]+$', 'Enter a valid first name. Only letters, spaces, and hyphens are allowed.', code='invalid_first_name')])),
                ('last_name', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[A-Za-z\\s-]+$', 'Enter a valid last name. Only letters, spaces, and hyphens are allowed.', code='invalid_last_name')])),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('job_title', models.CharField(choices=[('GD', 'General Director'), ('VD', 'Vice Director'), ('MN', 'Manager'), ('SP', 'Specialist'), ('AS', 'Assistant')], max_length=255)),
                ('content_type', models.ForeignKey(blank=True, limit_choices_to=models.Q(models.Q(('app_label', 'TestTask'), ('model', 'subsidiary')), models.Q(('app_label', 'TestTask'), ('model', 'contractor')), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ContractRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('GD', 'General Director'), ('VD', 'Vice Director'), ('MN', 'Manager'), ('SP', 'Specialist'), ('AS', 'Assistant')], max_length=2)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='TestTask.contract')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract_roles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='contract',
            name='organization_do',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts_do', to='TestTask.subsidiary'),
        ),
        migrations.AddField(
            model_name='contract',
            name='organization_po',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts_po', to='TestTask.contractor'),
        ),
    ]