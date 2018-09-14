from django.db import models


class Company(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'company'
