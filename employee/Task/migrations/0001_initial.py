# Generated by Django 5.0.1 on 2024-01-30 02:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('IN PROGRESS', 'IN PROGRESS'), ('COMPLETED', 'COMPLETED')], max_length=50)),
                ('assigned_to', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
