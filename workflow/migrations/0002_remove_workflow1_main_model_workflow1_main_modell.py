# Generated by Django 4.1.7 on 2024-02-01 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workflow1',
            name='Main_model',
        ),
        migrations.AddField(
            model_name='workflow1',
            name='Main_modell',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
