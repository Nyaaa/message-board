from django.db import migrations


def preload(apps, schema_editor):
    category = apps.get_model('boardapp', 'Category')
    names = ['Tanks', 'Healers', 'DDs', 'Traders', 'Guildmasters', 'Questgivers',
             'Blacksmiths', 'Leathersmiths', 'Potionbrewers', 'Spellmasters']
    bulk = [category(name=i, name_en=i) for i in names]
    category.objects.bulk_create(bulk)


class Migration(migrations.Migration):
    dependencies = [
        ('boardapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(preload),
    ]
