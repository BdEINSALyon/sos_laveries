# Generated by Django 2.1.3 on 2018-11-06 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nom du batiment')),
                ('active', models.BooleanField(verbose_name='Bâtiment ouvert (Possible de soumettre un problème)')),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, verbose_name='Numéro machine')),
                ('serial_number', models.CharField(max_length=30, verbose_name='Numéro de série')),
                ('active', models.BooleanField(verbose_name='Machine active ? Possible de soumettre un problème ?')),
                ('type', models.CharField(choices=[('L6', 'Lave-Linge 6Kg'), ('L10', 'Lave-Linge 6Kg'), ('S', 'Sèche-Linge'), ('M', 'Monnayeur')], max_length=3)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.Building', verbose_name='Batiment')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insa_email', models.EmailField(max_length=254)),
                ('last_name', models.CharField(max_length=255, verbose_name='Nom')),
                ('first_name', models.CharField(max_length=255, verbose_name='Prénom')),
                ('room', models.CharField(blank=True, max_length=10, null=True, verbose_name='Chambre')),
                ('phone_number', models.CharField(max_length=12, verbose_name='Numéro de téléphone')),
                ('problem_type', models.IntegerField(choices=[('1', 'Le linge est bloqué dans la machine (the laundry is stuck inside the machine)'), ('2', "J'ai mis un jeton mais le cycle n'a pas démarré (I inserted a coin but the cycle didn't start)"), ('3', 'La laverie est innondée (the laundry is flooded)'), ('4', 'Le monnayeur a été fracturé (the change machine has been broken into)'), ('0', 'Autre/Other')])),
                ('number_token_lost', models.IntegerField(default=0, verbose_name='Nombre de jetons perdus')),
                ('user_comment', models.TextField(verbose_name='Commentaire')),
                ('date_submission', models.DateTimeField(auto_now_add=True)),
                ('state', models.IntegerField(choices=[('0', 'Nouveau'), ('1', 'Accepté'), ('2', 'Refusé'), ('3', 'Terminé (Jetons rendus)')], default=0, verbose_name='Etat')),
                ('number_token_refund', models.IntegerField(default=0, verbose_name='Nombre de jetons rendus')),
                ('staff_comment', models.TextField(verbose_name='Commentaire staff (envoyé par email)')),
                ('date_treatment', models.DateTimeField(default=None)),
                ('date_refund', models.DateTimeField(default=None)),
                ('machine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='problem.Machine')),
            ],
        ),
    ]
