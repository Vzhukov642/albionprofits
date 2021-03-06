# Generated by Django 3.0.8 on 2020-08-26 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keys',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('key', models.TextField()),
            ],
            options={
                'db_table': 'keys',
                'unique_together': {('key', 'id')},
            },
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ip', models.TextField()),
                ('auth_key', models.TextField()),
                ('user_agent', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='MarketHistory',
        ),
        migrations.DeleteModel(
            name='MarketOrders',
        ),
        migrations.DeleteModel(
            name='MarketStats',
        ),
    ]
