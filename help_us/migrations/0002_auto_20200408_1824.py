# Generated by Django 2.2.1 on 2020-04-08 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help_us', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workrequest',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='workrequest',
            name='skills',
            field=models.TextField(max_length=23433),
        ),
    ]
