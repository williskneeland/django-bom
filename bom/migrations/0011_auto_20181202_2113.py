# Generated by Django 2.1.3 on 2018-12-02 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bom', '0010_auto_20181202_0733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermeta',
            name='google_drive_parent',
        ),
        migrations.AddField(
            model_name='organization',
            name='google_drive_parent',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
    ]
