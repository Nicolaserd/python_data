
from django.db import models

class Dashboard(models.Model):
    area = models.CharField(max_length=120)
    nombre = models.CharField(max_length=200)
    fuente = models.CharField(max_length=120, blank=True, null=True)
    linkapowerbi = models.URLField()
    esprivado = models.BooleanField(default=False)
    notebook_path = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['area','nombre']

    def __str__(self):
        return f"{self.area} - {self.nombre}"
