# Generated by Django 4.1.7 on 2023-04-03 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0003_post_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Сategories'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'permissions': [('accept_comment', 'Can accept Comment')], 'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='accepted',
            field=models.BooleanField(default=False, verbose_name='Accepted'),
        ),
    ]
