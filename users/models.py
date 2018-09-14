from django.db import models


class Profile(models.Model):
    TYPE_SUPPLIER = 'supplier'
    TYPE_BUYER = 'buyer'
    USER_TYPE_CHOICES = (
        (TYPE_SUPPLIER, 'Supplier / Owner'),
        (TYPE_BUYER, 'Buyer')
    )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES, default=TYPE_SUPPLIER)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'profile'
