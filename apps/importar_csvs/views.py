import logging

logging.basicConfig(filename='importar_csvs_log.log', level=logging.DEBUG)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

import io
import csv

from datetime import datetime
from .models import csv_to_list
from .forms import CsvModelForm
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
                
                celula = Celula().find_and_save(item, acao, fonte, natureza, pi, plano, ptres, ugEx, ugRes)
            
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


