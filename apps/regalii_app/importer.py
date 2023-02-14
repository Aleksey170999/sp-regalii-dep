import os
import pandas as pd
from django.conf import settings
from django.db import IntegrityError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .models import Regalia, Operation


class RegaliaImporter():
    # excel = pd.read_excel('regs.xlsx', 'Доделать_25.08')
    _scope = ['https://www.googleapis.com/auth/spreadsheets']
    _book_name = 'Лист8'
    _sheet_id = '11oyFJ_wKGDaR9kS-0_ThSH-K6htguHHbgekiUf49OQg'  # Все

    def __init__(self, ins=None, file=None, f=None):
        self.ins = ins
        self.file = file
        self.f = f
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self._scope)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    settings.GOOGLE_CREDENTIALS_FILE, self._scope)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        self.creds = creds

    def get_values(self):
        service = build('sheets', 'v4', credentials=self.creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self._sheet_id, range=f"ДОП СПБ-23!A{self.f}:C400").execute()
        values = result.get('values', [])

        return values


    def import_one_object(self):
        operation = Operation.objects.create()

        print(f"Импортирую: {self.ins['fio']}")
        rank = ''
        en_regalia = ''

        if '[' in self.ins['regalia']:
            s = self.ins['regalia'].split('[')
            regalia = s[0].strip()
            en_regalia = "[" + s[1]
            city = f"{regalia.split('(')[1].strip()[:-1]}"
            fio = self.ins['fio']
            spl_fio = fio.split()
            first_name = spl_fio[1]
            second_name = spl_fio[0]
            thi_name = spl_fio[2] if len(spl_fio) > 2 else ''
            rank = f"{regalia.split(self.ins['fio'])[0].strip()}" if regalia.split(self.ins['fio'])[0] != '' else ''
        else:
            regalia = self.ins['regalia']
            fio = self.ins['fio']
            spl_fio = fio.split()
            first_name = spl_fio[1]
            second_name = spl_fio[0]
            thi_name = spl_fio[2] if len(spl_fio) > 2 else ''
            city = f"{regalia.split('(')[1].strip()[:-1]}"
            rank = f"{regalia.split(self.ins['fio'])[0].strip()}" if regalia.split(self.ins['fio'])[0] != '' else ''

        try:
            Regalia.objects.create(full_name=fio,
                                   first_name=first_name,
                                   second_name=second_name,
                                   third_name=thi_name,
                                   rank=str(rank),
                                   city=str(city),
                                   regalia=regalia,
                                   en_regalia=en_regalia,
                                   operation=operation).save()
            print(f"Импортировано: {self.ins['fio']}")
            return Regalia.objects.last()

        except IntegrityError:
            print("---ОШИБКА: Данные уже записаны в базу, пропускаю...")

    def import_objects(self):
        values = self.get_values()
        counter = 0
        operation = Operation.objects.create()

        for ins in values:
            try:
                print(f"Импортирую: {ins[0]}")

                rank = ''
                en_regalia = ''

                if '[' in ins[2]:
                    s = ins[2].split('[')
                    regalia = s[0].strip()
                    en_regalia = "[" + s[1]
                    city = f"{regalia.split('(')[1].strip()[:-1]}"
                    fio = ins[0]
                    spl_fio = fio.split()
                    first_name = spl_fio[1]
                    second_name = spl_fio[0]
                    thi_name = spl_fio[2] if len(spl_fio) > 2 else ''
                    rank = f"{regalia.split(ins[0])[0].strip()}" if regalia.split(ins[0])[0] != '' else ''
                else:
                    regalia = ins[2]
                    fio = ins[0]
                    spl_fio = fio.split()
                    first_name = spl_fio[1]
                    second_name = spl_fio[0]
                    thi_name = spl_fio[2] if len(spl_fio) > 2 else ''
                    city = f"{regalia.split('(')[1].strip()[:-1]}"
                    rank = f"{regalia.split(ins[0])[0].strip()}" if regalia.split(ins[0])[0] != '' else ''

                try:
                    Regalia.objects.create(full_name=fio,
                                           first_name=first_name,
                                           second_name=second_name,
                                           third_name=thi_name,
                                           rank=str(rank),
                                           city=str(city),
                                           regalia=regalia,
                                           en_regalia=en_regalia,
                                           operation=operation).save()
                except IntegrityError:
                    print("---ОШИБКА: Данные уже записаны в базу, пропускаю...")
                    continue
            except IndexError:
                pass
            counter += 1
            try:
                print(f"Импортировано: {ins[0]}")
            except IndexError:
                pass
        print("\n" + f"Импортировано {counter} регалий")

    def import_from_excel(self):
        operation = Operation.objects.create()

        excel = pd.read_excel(self.file, 'Sheet1')
        for ins in excel.values:
            print(f"Импортирую: {ins[0]}")
            rank = ''
            en_regalia = ''
            print(ins)
            if '[' in ins[2]:
                s = ins[2].split('[')
                regalia = s[0].strip()
                en_regalia = "[" + s[1]
                city = f"{regalia.split('(')[1].strip()[:-1]}"
                fio = ins[0]
                spl_fio = fio.split()
                first_name = spl_fio[1]
                second_name = spl_fio[0]
                thi_name = spl_fio[2] if len(spl_fio) > 2 else ''
                rank = f"{regalia.split(ins[0])[0].strip()}" if regalia.split(ins[0])[0] != '' else ''
            else:
                regalia = ins[2]
                fio = ins[0]
                spl_fio = fio.split()
                first_name = spl_fio[1]
                second_name = spl_fio[0]
                thi_name = spl_fio[2] if len(spl_fio) > 2 else ''
                city = f"{regalia.split('(')[1].strip()[:-1]}"
                rank = f"{regalia.split(ins[0])[0].strip()}" if regalia.split(ins[0])[0] != '' else ''

            try:
                Regalia.objects.create(full_name=fio,
                                       first_name=first_name,
                                       second_name=second_name,
                                       third_name=thi_name,
                                       rank=str(rank),
                                       city=str(city),
                                       regalia=regalia,
                                       en_regalia=en_regalia,
                                       operation=operation).save()
            except IntegrityError:
                print("---ОШИБКА: Данные уже записаны в базу, пропускаю...")
                continue

            print(f"Импортировано: {ins[0]}")
        qs = Regalia.objects.filter(operation=operation)
        return qs
