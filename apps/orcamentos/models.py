from django.db import models

from apps.pi.models import Base

# Create your models here.

class Orcamento(Base):
    def __str__(self):
        return self.codigo

    class Meta:
        db_table = 'orcamentos'
        managed = False

    def find_and_save(self, codigo, descricao):
        try:
            #print(codigo)
            obj = __class__.objects.get(codigo=codigo)
            return obj
        except:
            self.codigo = codigo
            self.descricao = descricao
            self.save()
            return self
