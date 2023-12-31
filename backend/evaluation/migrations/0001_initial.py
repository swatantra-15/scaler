# Generated by Django 4.2.6 on 2023-10-31 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub1', models.IntegerField(default=0)),
                ('sub2', models.IntegerField(default=0)),
                ('sub3', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('locked', models.BooleanField(default=False)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluation.mentor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluation.student')),
            ],
        ),
    ]
