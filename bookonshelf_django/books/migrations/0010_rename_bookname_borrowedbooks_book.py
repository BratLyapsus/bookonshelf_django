# Generated by Django 5.0.4 on 2024-05-09 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_borrowedbooks_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrowedbooks',
            old_name='bookname',
            new_name='book',
        ),
    ]