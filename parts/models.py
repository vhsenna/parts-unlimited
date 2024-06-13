from django.db import models


class Part(models.Model):
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=30)
    description = models.TextField(max_length=1024)
    weight_ounces = models.IntegerField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "part"
