# Generated by Django 2.2 on 2019-04-07 12:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('problem', '0004_auto_20190325_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='type',
            field=models.IntegerField(
                choices=[(0, 'Lave-Linge 6Kg'), (1, 'Lave-Linge 10Kg'), (2, 'Sèche-Linge'), (3, 'Monnayeur')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='problem_type',
            field=models.IntegerField(
                choices=[(0, 'Le linge est bloqué dans la machine (the laundry is stuck inside the machine)'), (
                1, "J'ai mis un jeton mais le cycle n'a pas démarré (I inserted a coin but the cycle didn't start)"),
                         (2, 'La laverie est innondée (the laundry is flooded)'),
                         (3, 'Le monnayeur a été fracturé (the change machine has been broken into)'),
                         (4, 'Autre/Other')]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='state',
            field=models.IntegerField(choices=[(0, 'Nouveau'), (1, 'Accepté'), (2, 'Refusé'), (3, 'Clos')], default=0,
                                      verbose_name='Etat'),
        ),
    ]