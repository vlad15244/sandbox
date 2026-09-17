from django.db import models

# Create your models here.
class MyModels(models.Model):
    Name = models.CharField(max_length=45, verbose_name="Имя")

    def __str__(self):
        return f'{self.Name}'
