import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from django.conf import settings
from psycopg2 import IntegrityError

from apps.regalii_app.models import Regalia


def g_auth(scope):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scope)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_CREDENTIALS_FILE, scope)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def prepare_text(data):
    rank = data['rank']
    fio = data['fio']
    city = data['city']
    fir_name = data['fir_name']
    sec_name = data['sec_name']
    thi_name = data['thi_name'] if data['thi_name'] != '' else None
    en_regalia = data['en_regalia']
    ru_regalia = data['ru_regalia']
    text = ''
    if rank == "":
        # На случай фамилий из двух слов без тире
        text = f"{rank} {fio.split()[0]}" + "\n" + f"{' '.join(fio.split()[1:])}" + "\n" + f"({city})"
        # text = f"{sec_name}" + "\n" + f"{fir_name} {thi_name}" + "\n" + f"({city})"
    else:
        if 3 <= len(rank) <= 16:
            if thi_name is not None:
                if len(sec_name) >= 15:
                    text = f"{rank}" + "\n" + f"{fio.split()[0]}" + "\n" + f"{fio.split()[1]} {fio.split()[2]}" + "\n" + f"({city})"
                else:
                    # На случай фамилий из двух слов без тире
                    # text = f"{rank} {fio.split()[0]}" + "\n" + f"{' '.join(fio.split()[1:])}" + "\n" + f"({city})"
                    text = f"{rank} {fio.split()[0]}" + "\n" + f"{fio.split()[1]} {fio.split()[2]}" + "\n" + f"({city})"
            else:
                if en_regalia:
                    text = f"{rank + ' ' + fio}" + "\n" + f"({city})" + "\n" + f"{en_regalia.split('(')[0].strip()}" + "\n" + f"({en_regalia.split('(')[1]}"
                else:
                    text = f"{rank}" + "\n" + f"{fio}" + "\n" + f"({city})"
        if 17 <= len(rank) <= 30:
            if thi_name is not None:
                text = f"{rank}" + "\n" + f"{fio.split()[0]}" + "\n" + f"{fio.split()[1]} {fio.split()[2]}" + "\n" + f"({city})"
            else:
                if en_regalia:
                    text = f"{rank} " + "\n" + f"{fio}"  + f" ({city})" + "\n" + f"{en_regalia.split('(')[0].strip()}" + "\n" + f" ({en_regalia.split('(')[1]}"
                else:
                    text = f"{rank}" + "\n" + f"{fio.split()[0]} {fio.split()[1]}" + "\n" + f"{city}"


        if 31 <= len(rank) < 40:
            if thi_name is not None:
                text = f"{rank.split(',')[0]}," + "\n" + f"{','.join(rank.split(',')[1:])}" + "\n" + f"{fio}" + "\n" + f"({city})"
            else:
                text = f"{rank}" + "\n" + f"{fio.split()[0]} {fio.split()[1]}" + "\n" + f"{city}"

        if len(rank) >= 40:
            if thi_name is not None:
                text = f"{rank.split(',')[0]}," + "\n" + f"{rank.split(',')[1]}," + f"{rank.split(',')[2]}" + "\n" + f"{fio}" + "\n" + f"({city})"
            else:
                if len(en_regalia) > 1:
                    text = f"{ru_regalia.split('(')[0].strip()}" + "\n" + f"({ru_regalia.split('(')[-1]}" + "\n" + f"{en_regalia.split('(')[0].strip()}" + "\n" + f"({en_regalia.split('(')[1]}"
                else:
                    text = f"{rank}" + "\n" + f"{fio.split()[0]} {fio.split()[1]}" + "\n" + f"({city})"
    return text


def draw_text(text, font, draw, size):
    i = 0
    if len(text.split("\n")) == 4:
        i = -30
    if len(text.split("\n")) == 3:
        i = -27 if size == (315, 177) else -22
    if len(text.split("\n")) == 2:
        i = -10

    if len(text.split("\n")) == 3:
        i = -27 if size == (315, 177) else -22

        for str in text.split("\n"):
            if 'None' in str:
                str = str[0:-4]
            draw.text(
                font=font,
                xy=(size[0] / 2, size[1] / 2 + i),
                text=str,
                fill=(1, 0, 0),
                anchor="mm"
            )
            if size == (315, 177):
                i += 22
            else:
                i += 20
    elif len(text.split("\n")) == 4:
        i = -30
        for str in text.split("\n"):
            draw.text(
                font=font,
                xy=(size[0] / 2, size[1] / 2 + i),
                text=str,
                fill=(1, 0, 0),
                anchor="mm"
            )
            if size == (315, 177):
                i += 23
            else:
                i += 19
    elif len(text.split("\n")) == 2:
        i = -10
        for str in text.split("\n"):
            draw.text(
                font=font,
                xy=(size[0] / 2, size[1] / 2 + i),
                text=str,
                fill=(1, 0, 0),
                anchor="mm"
            )
            if size == (315, 177):
                i += 22
            else:
                i += 20

def create_regalia_record(excel_file, operation):
    for ins in excel_file.values:
        import_regalia(ins, operation)


def import_regalia(ins, operation):
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
                                   operation=operation)
            print(f"Импортировано: {ins[0]}")
            return Regalia.objects.last()
        except IntegrityError:

            print("---ОШИБКА: Данные уже записаны в базу, пропускаю...")
    except IndexError:
        pass