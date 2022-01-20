from django.db import models
from django.contrib.auth.models import User


class MyWallet(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    admission = models.IntegerField()
    consumption = models.IntegerField()
    description = models.TextField()
    users_date = models.TextField()
    insert_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'my_wallet'
