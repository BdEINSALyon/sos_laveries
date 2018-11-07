from django.db import models

TYPE_MACHINE = [
    ('L6', "Lave-Linge 6Kg"),
    ('L10', "Lave-Linge 6Kg"),
    ('S', 'Sèche-Linge'),
    ('M', 'Monnayeur')
]

TYPE_PROBLEM = [
    (1, "Le linge est bloqué dans la machine (the laundry is stuck inside the machine)"),
    (2, "J'ai mis un jeton mais le cycle n'a pas démarré (I inserted a coin but the cycle didn't start)"),
    (4, 'La laverie est innondée (the laundry is flooded)'),
    (5, 'Le monnayeur a été fracturé (the change machine has been broken into)'),
    (6, 'Autre/Other'),
]

ETAT_TICKET = [
    (0, "Nouveau"),
    (1, "Accepté"),
    (2, 'Refusé'),
    (3, 'Terminé (Jetons rendus)')
]

# Create your models here.
class Building(models.Model):
    name=models.CharField(max_length=30, verbose_name="Nom du batiment")
    active=models.BooleanField(verbose_name="Bâtiment ouvert (Possible de soumettre un problème)")
    def __str__(self):
        return "Bâtiment " + self.name

class Machine(models.Model):
    number=models.CharField(max_length=10, verbose_name="Numéro machine", null=False, blank=False)
    serial_number=models.CharField(max_length=30, verbose_name="Numéro de série")
    active=models.BooleanField(verbose_name="Machine active ? Possible de soumettre un problème ?", null=False, blank=False)
    building=models.ForeignKey('Building', on_delete=models.CASCADE, verbose_name="Batiment", null=False, blank=False)
    type=models.CharField(max_length=3, choices=TYPE_MACHINE, null=False, blank=False)
    def __str__(self):
        return "Bâtiment " + self.building.name + " - Machine n° " + self.number

class Ticket(models.Model):
    insa_email=models.EmailField()
    last_name = models.CharField(verbose_name='Nom', blank=False, max_length=255, null=False)
    first_name = models.CharField(verbose_name='Prénom', blank=False, max_length=255, null=False)
    room = models.CharField(verbose_name='Chambre', blank=True, max_length=10, null=True)
    phone_number = models.CharField(verbose_name='Numéro de téléphone', blank=False, max_length=12, null=False)
    machine=models.ForeignKey('Machine', on_delete=models.SET_NULL, null=True)
    problem_type=models.IntegerField(choices=TYPE_PROBLEM, blank=False)
    number_token_lost = models.IntegerField(verbose_name="Nombre de jetons perdus", blank=False, default=0)
    user_comment=models.TextField(verbose_name="Commentaire", null=True, blank=True)
    date_submission = models.DateTimeField(auto_now_add=True)
    state=models.IntegerField(verbose_name="Etat", choices=ETAT_TICKET, blank=False, default=0)
    number_token_refund = models.IntegerField(verbose_name="Nombre de jetons rendus", blank=True, default=0, null=True)
    staff_comment = models.TextField(verbose_name="Commentaire staff (envoyé par email)", blank=True, null=True)
    date_treatment = models.DateTimeField(default=None, blank=True, null=True)
    date_refund = models.DateTimeField(default=None , blank=True, null=True)
    def __str__(self):
        return "Ticket #" + str(self.pk)
    @property
    def count_same_email(self):
        return Ticket.objects.filter(insa_email=self.insa_email).all().count()
