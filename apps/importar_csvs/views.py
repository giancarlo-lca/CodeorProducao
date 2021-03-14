import logging

logging.basicConfig(filename='importar_csvs_log.log', level=logging.DEBUG)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

import io
import csv
import xlrd

from datetime import datetime
from .models import csv_to_list
from .forms import CsvModelForm, XlsxModelForm
from decimal import *

from django.shortcuts import render

from apps.acao_governo.models import AcaoGoverno
from apps.orcamentos.models import Orcamento
from apps.ptres.models import Ptres
from apps.ug_executora.models import UGExecutora
from apps.ug_responsavel.models import UGResponsavel
from apps.pi.models import Pi
from apps.fonte_recursos.models import FonteRecurso
from apps.natureza_despesas.models import NaturezaDespesas

from apps.celulas.models import Celula


# Create your views here.
@login_required(login_url='/accounts/login/')
@staff_member_required
def upload_file_view(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # abra o arquivo
        try:
            logging.debug('lendo o arquivo')
            arquivo = io.TextIOWrapper(request.FILES['arquivo'])
            #print(nomeArquivo)
            # let's check if it is a csv file
            if not arquivo.name.endswith('.csv'):
                messages.error(request, 'Não é um arquivo CSV')
                return render(request, 'upload.html',{'form': form})
        
        # file = myfile.read().decode('utf-8-sig')
        # reader = csv.DictReader(io.StringIO(file), delimiter=';')
        # data = [line for line in reader]
            logging.debug('lendo o arquivo - csv_to_list')
            data = csv_to_list(arquivo)
            #print(data)
            #i = 1
            now = datetime.now()
            
        # dd/mm/YY H:M:S
            dt_string = now.strftime("%H:%M:%S")
            logging.debug('registrando o tempo inicial '+dt_string)
            # print("date and time =", dt_string)
            logging.debug('lendo cada linha do arquivo - for item in data:')
            for item in data:
                #print(i)
                #i+=1
                #acao = AcaoGoverno()
                logging.debug(item.get('codgov'))
                acao = AcaoGoverno().find_and_save(item.get('codgov'), item.get('acaogov'))
            # print(acao)
                plano = Orcamento().find_and_save(item.get('codplano'), item.get('plano'))
                ptres = Ptres().find_and_save(item.get('ptres'))
                fonte = FonteRecurso().find_and_save(item.get('codfonte'), item.get('fonte'))
                pi = Pi().find_and_save(item.get('codpi'), item.get('pi'))
                ugRes = UGResponsavel().find_and_save(item.get('codugres'), item.get('ugres'))
                ugEx = UGExecutora().find_and_save(item.get('codugex'), item.get('ugex'))
                natureza = NaturezaDespesas().find_and_save(item.get('codnatureza'), item.get('natureza'))
                
                celula = Celula().find_and_save_csv(item, acao, fonte, natureza, pi, plano, ptres, ugEx, ugRes)
            
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")

            logging.debug('registrando o tempo final '+dt_string)
            # print("date and time =", dt_string)
            # Percorrer o arquivo
            
            # Para cada linha chama um método find_and_save (Da classe base) passando parametros conheciados
            messages.success(request, 'Arquivo importado com sucesso.') 
            return render(request, 'upload.html',{'form': form})
        
        except Warning as e:
            logging.debug('Error occurred ' + str(e))
            messages.error(request, 'Erro ao importar arquivo') 
            form = CsvModelForm()
            return render(request, 'upload.html', {'form': form})

    # print(form)
    return render(request, 'upload.html', {'form': form})


@login_required(login_url='/accounts/login/')
@staff_member_required
def upload_file_view_xls(request):
    form = XlsxModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # abra o arquivo
        try:
            logging.debug('lendo o arquivo')
            arquivo = request.FILES['arquivo']
            # print(arquivo)
            # let's check if it is a csv file
            if not arquivo.name.endswith('.xlsx') and not arquivo.name.endswith('.xls'):
                messages.error(request, 'Não é um arquivo XLS ou XLSX')
                return render(request, 'upload_xlsx.html',{'form': form})
        
            # Abre o arquivo
            xls = xlrd.open_workbook(file_contents=arquivo.read())
            # Pega a primeira planilha do arquivo
            plan = xls.sheet_by_index(0)
            
            now = datetime.now()
            
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%H:%M:%S")
            logging.debug('registrando o tempo inicial '+dt_string)
            
            for row in range(1, plan.nrows):

                codGov = plan.row(row)[0].value
                acaoGov = plan.row(row)[1].value
                acao = AcaoGoverno().find_and_save(codGov, acaoGov)
                                 
                codPlano = plan.row(row)[2].value
                planoDesc = plan.row(row)[3].value
                plano = Orcamento().find_and_save(codPlano, planoDesc)
               
                ptresId = plan.row(row)[4].value
                ptres = Ptres().find_and_save(ptresId)
                
                codUgEx = plan.row(row)[5].value
                ugExDesc = plan.row(row)[6].value
                ugEx = UGExecutora().find_and_save(codUgEx, ugExDesc)

                codUgRes = plan.row(row)[7].value
                ugResDesc = plan.row(row)[8].value
                ugRes = UGResponsavel().find_and_save(codUgRes, ugResDesc)

                codPi = plan.row(row)[9].value
                piDesc = plan.row(row)[10].value
                pi = Pi().find_and_save(codPi, piDesc)

                codFonte = plan.row(row)[11].value
                fonteDesc = plan.row(row)[12].value
                fonte = FonteRecurso().find_and_save(codFonte, fonteDesc)
 
                codNatureza = plan.row(row)[13].value
                naturezaDesc = plan.row(row)[14].value
                natureza = NaturezaDespesas().find_and_save(codNatureza, naturezaDesc)

                dotacao = plan.row(row)[15].value
                credito = plan.row(row)[16].value
                despEmp = plan.row(row)[17].value
                despPagas = plan.row(row)[18].value

                item = {}
                item['dotacao'] = dotacao
                item['credito'] = credito
                item['despEmp'] = despEmp
                item['despPagas'] = despPagas

                # print("{:.2f}".format(item[0]))
                # print("{:.2f}".format(item[1]))
                # print("{:.2f}".format(item[2]))
                # print("{:.2f}".format(item[3]))
                celula = Celula().find_and_save_xls(item, acao, fonte, natureza, pi, plano, ptres, ugEx, ugRes)
            
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")

            logging.debug('registrando o tempo final '+dt_string)
           
            messages.success(request, 'Arquivo importado com sucesso.') 
            return render(request, 'upload_xlsx.html',{'form': form})
        
        except Warning as e:
            logging.debug('Error occurred ' + str(e))
            messages.error(request, 'Erro ao importar arquivo') 
            form = XlsxModelForm()
            return render(request, 'upload_xlsx.html', {'form': form})

    return render(request, 'upload_xlsx.html', {'form': form})