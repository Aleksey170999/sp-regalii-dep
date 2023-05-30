import pandas as pd
from django.db import IntegrityError
from googleapiclient.discovery import build

from .models import Regalia, Operation
from .utils import g_auth, create_regalia_record, import_regalia


class RegaliaImporter():

    def __init__(self, ins=None, file=None, f=None):
        self.ins = ins
        self.file = file
        self.f = f
        self._scope = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = g_auth(self._scope)
        self._book_name = 'РСБ и АА+ЭГ'
        self._sheet_id = '11oyFJ_wKGDaR9kS-0_ThSH-K6htguHHbgekiUf49OQg'

    def get_values(self):
        service = build('sheets', 'v4', credentials=self.creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self._sheet_id, range=f"{self._book_name}!A{self.f}:C400").execute()
        values = result.get('values', [])

        return values


    def import_one_object(self):
        operation = Operation.objects.create()
        return import_regalia(self.ins, operation)


    def import_objects(self):
        values = self.get_values()
        counter = 0
        operation = Operation.objects.create()

        for ins in values:
            import_regalia(ins, operation)
            counter += 1

        print("\n" + f"Импортировано {counter} регалий")

    def import_from_excel(self):
        operation = Operation.objects.create()
        excel = pd.read_excel(self.file, 'Sheet1')
        create_regalia_record(excel_file=excel,
                              operation=operation)
        return Regalia.objects.filter(operation=operation)
