from django.db import models


# Create your models here.

class AccountModel(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return "charges = {0}, total = {1}".format(self.id, self.total)

    class Meta:
        db_table = 'accounts'


class ChargeModel(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    account = models.ForeignKey(AccountModel, related_name='charge', on_delete=models.CASCADE)

    def __str__(self):
        return "value = {0}, date = {1}".format(self.value, self.date)

    class Meta:
        db_table = 'charges'



