# Generated by Django 5.0.1 on 2024-01-10 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categpry',
            new_name='Category',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='categpry_name',
            new_name='category_name',
        ),
    ]
