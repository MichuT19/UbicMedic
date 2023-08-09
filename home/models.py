
from django.db import models

class Sexo(models.Model):
    id_sexo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50,verbose_name = 'Sexo')
    class Meta:
        managed = True
        db_table = 'Sexo'
        verbose_name = 'Sexo'
        verbose_name_plural = 'Sexo'
    def __str__(self):
        return self.descripcion
    

  



  




