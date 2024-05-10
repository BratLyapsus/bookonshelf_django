# Generated by Django 5.0.4 on 2024-05-07 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_genres_genre_alter_languages_language_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowedBooks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registrationnumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.books')),
            ],
            options={
                'verbose_name': 'Ваша книга',
                'verbose_name_plural': 'Ваши книги',
            },
        ),
    ]
