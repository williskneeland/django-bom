# Generated by Django 4.0.4 on 2022-04-29 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bom', '0044_alter_assembly_id_alter_assemblysubparts_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartClassWorkflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PartClassWorkflowState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('is_final_state', models.BooleanField(default=False)),
                ('assigned_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subpart',
            name='alternates',
            field=models.ManyToManyField(to='bom.partrevision'),
        ),
        migrations.CreateModel(
            name='PartWorkflowInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_state', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='bom.partclassworkflowstate')),
                ('currently_assigned_users', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('part', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='bom.part')),
                ('workflow', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='bom.partclassworkflow')),
            ],
        ),
        migrations.CreateModel(
            name='PartClassWorkflowStateTransition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction_in_workflow', models.CharField(default='forward', max_length=15)),
                ('source_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_state', to='bom.partclassworkflowstate')),
                ('target_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_state', to='bom.partclassworkflowstate')),
                ('workflow', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='bom.partclassworkflow')),
            ],
            options={
                'unique_together': {('source_state', 'target_state', 'workflow')},
            },
        ),
        migrations.CreateModel(
            name='PartClassWorkflowCompletedTransition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('notifying_next_users', models.BooleanField(default=True, verbose_name='Notifying next users')),
                ('completed_by', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('part', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='bom.part')),
                ('transition', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='bom.partclassworkflowstatetransition')),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
        migrations.AddField(
            model_name='partclassworkflow',
            name='initial_state',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='bom.partclassworkflowstate'),
        ),
        migrations.AddField(
            model_name='partclass',
            name='workflow',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bom.partclassworkflow'),
        ),
    ]
