from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('owner', 'FieldOwner'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=22, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


class Maydon(models.Model):
    name = models.CharField(max_length=222)
    address = models.TextField()
    contact = models.CharField(max_length=222)
    images = models.ImageField(upload_to='maydon_img/', blank=True, null=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maydonlar')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name


class Bron(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    maydon = models.ForeignKey(Maydon, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.maydon.name} bronqilgan {self.user.username} {self.id}"



