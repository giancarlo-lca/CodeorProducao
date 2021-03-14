from django.db import models

import csv

class Csv(models.Model):
    arquivo = models.FileField(upload_to='csvs')

    class Meta:
        managed = False

class Xls(models.Model):
    arquivo = models.FileField(upload_to='xlsx')

    class Meta:
        managed = False


def csv_to_list(filename: str) -> list:
    """Receive an csv filename and returns rows of file with an list"""
    reader = csv.DictReader(filename, delimiter=';')
    csv_data = [line for line in reader]
    return csv_data


