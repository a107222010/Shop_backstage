# Generated by Django 2.2.10 on 2021-10-09 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_menu', '0003_auto_20211010_0020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productsize',
            old_name='product_id',
            new_name='product',
        ),
    ]