# Generated by Django 2.2.9 on 2020-02-22 03:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bom', '0033_auto_20200203_0618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='number_class',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='number_class', to='bom.PartClass'),
        ),
        migrations.AlterField(
            model_name='part',
            name='number_item',
            field=models.CharField(blank=True, default=None, max_length=128, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')]),
        ),
        migrations.AlterField(
            model_name='part',
            name='number_variation',
            field=models.CharField(blank=True, default=None, max_length=2, null=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')]),
        ),
    ]
