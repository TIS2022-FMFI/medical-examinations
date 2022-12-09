# Generated by Django 4.1.3 on 2022-12-09 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rule', '0001_initial'),
        ('examinationType', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RulesExamination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examinationTypeId', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='examinationType.examinationtype')),
                ('ruleId', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rule.rule')),
            ],
        ),
    ]
