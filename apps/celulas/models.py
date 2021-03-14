import logging
logging.basicConfig(filename='celulas_log.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

from django.db import models

import decimal

from apps.acao_governo.models import AcaoGoverno
from apps.orcamentos.models import Orcamento
from apps.ptres.models import Ptres
from apps.ug_executora.models import UGExecutora
from apps.ug_responsavel.models import UGResponsavel
from apps.pi.models import Pi
from apps.fonte_recursos.models import FonteRecurso
from apps.natureza_despesas.models import NaturezaDespesas

# Create your models here.
class Celula(models.Model):
    acao = models.ForeignKey(AcaoGoverno, on_delete=models.DO_NOTHING)
    plano = models.ForeignKey(Orcamento, on_delete=models.DO_NOTHING)
    ptres = models.ForeignKey(Ptres, on_delete=models.DO_NOTHING)
    ugresp = models.ForeignKey(UGResponsavel, on_delete=models.DO_NOTHING)
    ugex = models.ForeignKey(UGExecutora, on_delete=models.DO_NOTHING)
    pi = models.ForeignKey(Pi, on_delete=models.DO_NOTHING)
    fonte = models.ForeignKey(FonteRecurso, on_delete=models.DO_NOTHING)
    natureza = models.ForeignKey(NaturezaDespesas, on_delete=models.DO_NOTHING)

    dotacao = models.DecimalField(max_digits=15, decimal_places=2)
    credito = models.DecimalField(max_digits=15, decimal_places=2)
    despesasEmp = models.DecimalField(max_digits=15, decimal_places=2)
    despesasPagas = models.DecimalField(max_digits=15, decimal_places=2)

    descricao = models.CharField(max_length=150, null=True, blank=True)
    observacao = models.TextField(max_length=300, null=True, blank=True)
    
    class Meta:
        db_table = 'celulas'
        constraints = [
            models.UniqueConstraint(fields=['acao', 'plano', 'ptres', 
                                            'ugresp', 'ugex', 'pi', 'fonte',
                                             'natureza'],name='unique_celula'),
        ]
    
    def __str__(self):
        return self.pi.descricao
    

    def descricao_(self):
        if self.descricao == None:
            return self.natureza.descricao
        else:
            return self.descricao


    def total_planejado(self):
        total = decimal.Decimal(0.00)

        for planejamento in self.planejamento_set.all():
            if planejamento.status.upper() not in ('EMPENHADO', 'PAGO', 'CANCELADO'): 
                total+= decimal.Decimal(planejamento.valor)

        return total
    
    def formatToDecimal(valor):
        return 0 if valor == '' else decimal.Decimal(valor.replace(".", "").replace(",",".")
                                                          .replace("(","").replace(")",""))

    def find_and_save_csv(self, item, acao, fonte, natureza, pi, plano, ptres, ugex, ugresp):
        try:
            obj = __class__.objects.get(acao=acao, fonte=fonte, natureza=natureza, pi=pi,
                                         plano=plano, ptres=ptres, ugex=ugex, ugresp=ugresp)
            #print(obj)

            obj.dotacao = 0 if item.get('dotacao') == '' else decimal.Decimal(item.get('dotacao').replace(".", "").replace(",",".")
                                                          .replace("(","").replace(")",""))
            obj.credito = 0 if item.get('credito') == '' else decimal.Decimal(item.get('credito').replace(".", "").replace(",",".")
                                                          .replace("(","").replace(")",""))
            obj.despesasEmp = 0 if item.get('desp_emp') == '' else decimal.Decimal(item.get('desp_emp').replace(".", "").replace(",",".")
                                                          .replace("(","").replace(")",""))
            obj.despesasPagas = 0 if item.get('desp_pagas') == '' else decimal.Decimal(item.get('desp_pagas').replace(".", "").replace(",",".")
                                                          .replace("(","").replace(")",""))
            obj.save()
            
            return obj.id
        except Exception as err:
            logger.error(err)
            # logging.info('Não encontrou e vai criar uma celula ' + str(err))
            self.acao = acao
            self.plano = plano
            self.ptres = ptres
            self.ugresp = ugresp
            self.ugex = ugex
            self.pi = pi
            self.fonte = fonte
            self.natureza = natureza

            self.dotacao = 0 if item.get('dotacao') == '' else decimal.Decimal(item.get('dotacao').replace(".", "").replace(",",".")
                                                          .replace("(","").replace(")",""))
            self.credito = 0 if item.get('credito') == '' else decimal.Decimal(item.get('credito').replace(".", "").replace(",",".")
                                                          .replace("(","").replace(")",""))
            self.despesasEmp = 0 if item.get('desp_emp') == '' else decimal.Decimal(item.get('desp_emp').replace(".", "").replace(",",".")
                                                          .replace("(","").replace(")",""))
            self.despesasPagas = 0 if item.get('desp_pagas') == '' else decimal.Decimal(item.get('desp_pagas').replace(".", "").replace(",",".")
                                                          .replace("(","").replace(")",""))
            #self.description = desc
            self.save()
            return self

    def find_and_save_xls(self, item, acao, fonte, natureza, pi, plano, ptres, ugex, ugresp):
        try:
            obj = __class__.objects.get(acao=acao, fonte=fonte, natureza=natureza, pi=pi,
                                         plano=plano, ptres=ptres, ugex=ugex, ugresp=ugresp)
            #print(obj)

            obj.dotacao = 0 if item['dotacao'] == '' else "{:.2f}".format(item['dotacao'])
            obj.credito = 0 if item['credito'] == '' else "{:.2f}".format(item['credito'])
            obj.despesasEmp = 0 if item['despEmp'] == '' else "{:.2f}".format(item['despEmp'])
            obj.despesasPagas = 0 if item['despPagas'] == '' else "{:.2f}".format(item['despPagas'])

            obj.save()
            return obj.id
     
        except Exception as err:
            logger.error(err)
            # logging.info('Não encontrou e vai criar uma celula ' + str(err))
            self.acao = acao
            self.plano = plano
            self.ptres = ptres
            self.ugresp = ugresp
            self.ugex = ugex
            self.pi = pi
            self.fonte = fonte
            self.natureza = natureza

            self.dotacao = 0 if item['dotacao'] == '' else "{:.2f}".format(item['dotacao'])
            # print(self.dotacao)
            self.credito = 0 if item['credito'] == '' else "{:.2f}".format(item['credito'])
            # print(self.credito)  
            self.despesasEmp = 0 if item['despEmp'] == '' else "{:.2f}".format(item['despEmp'])
            # print(self.despesasEmp)
            self.despesasPagas = 0 if item['despPagas'] == '' else "{:.2f}".format(item['despPagas'])
            # print(self.despesasPagas)
            #self.description = desc
            self.save()
            return self