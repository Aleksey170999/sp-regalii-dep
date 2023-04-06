from datetime import datetime
import os
from pathlib import Path
import zipfile
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

import boto3


class RegaliaGenerator:
    REGALII_DIR = Path(__file__).resolve().parent / 'generated'
    sizes = [(315, 177), (272, 98), (320, 107), (320, 80)]

    def __init__(self, qs=None, ins=None):
        self.qs = qs
        self.ins = ins

    def generate_one(self, ins):
        for size in self.sizes:
            font = ImageFont.truetype('apps/regalii_app/helios.ttf', 23, encoding="utf-8") if size == (
                315, 177) else ImageFont.truetype('apps/regalii_app/helios.ttf', 19, encoding="utf-8")
            im = Image.new('RGB', size, (232, 243, 249))
            self.generate_png(im=im, ins=ins, font=font, size=size)

    def generate_all(self):
        counter = 0
        for ins in self.qs:
            self.generate_one(ins)
            counter += 1
            ins.is_generated = True
            ins.save()
            print(ins.full_name)

    def generate_png(self, im, ins, font, size):
        draw = ImageDraw.Draw(im)
        data = self._get_data(ins)
        text = self.prepare_text(data)
        self.draw_text(text=text, font=font, im=im, draw=draw, size=size)
        self.save_png(data, im)

    def prepare_text(self, data):
        rank = data['rank']
        fio = data['fio']
        city = data['city']
        fir_name = data['fir_name']
        sec_name = data['sec_name']
        thi_name = data['thi_name'] if data['thi_name'] != '' else None
        en_regalia = data['en_regalia']
        ru_regalia = data['ru_regalia']
        text = ''
        print(data)
        if rank == "":
            # На случай фамилий из двух слов без тире
            # text = f"{rank} {fio.split()[0]}" + "\n" + f"{' '.join(fio.split()[1:])}" + "\n" + f"({city})"

            text = f"{sec_name}" + "\n" + f"{fir_name} {thi_name}" + "\n" + f"({city})"
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

    def _get_data(self, ins):
        fio = ins.full_name
        rank = ins.rank
        city = ins.city
        fir_name = ins.first_name
        sec_name = ins.second_name
        thi_name = ins.third_name if ins.third_name != '' else None
        en_regalia = ins.en_regalia
        ru_regalia = ins.regalia

        data = {"fio": fio,
                "rank": rank,
                "city": city,
                "fir_name": fir_name,
                "sec_name": sec_name,
                "thi_name": thi_name,
                "en_regalia": en_regalia,
                "ru_regalia": ru_regalia}

        return data

    def draw_text(self, text, font, im, draw, size):
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

    def save_png(self, data, im):
        path = f'/{self.REGALII_DIR}/'

        if im.size == (315, 177):
            i = 1
        if im.size == (272, 98):
            i = 2
        if im.size == (320, 107):
            i = 3
        if im.size == (320, 80):
            i = 4
        name = f'{data["sec_name"]}_{data["fir_name"][0]}{data["thi_name"][0]}_{i}.png' if data[
            "thi_name"] else f'{data["sec_name"]}_{data["fir_name"][0]}_{i}.png'
        if name in os.listdir(self.REGALII_DIR):
            name = f'{data["sec_name"]}_{data["fir_name"][0]}{data["thi_name"][0]}_{i}.png' if data[
            "thi_name"] else f'{data["sec_name"]}_{data["fir_name"][0]}_{i}_.png'
        im.save(path + name)

    def save_to_archive(self):
        archname = f'regalii_{datetime.now()}.zip'
        arch = zipfile.ZipFile(f'/{self.REGALII_DIR}/{archname}', 'w')

        files = os.listdir(f'apps/regalii_app/generated')

        for file in files:
            if file.endswith('.png'):
                arch.write(filename=f"apps/regalii_app/generated/{file}", compress_type=zipfile.ZIP_DEFLATED)
                os.remove(f"apps/regalii_app/generated/{file}")
        arch.close()
        return archname

    def get_url_to_archive(self, archname):
        file = f'apps/regalii_app/generated/{archname}'

        s3 = boto3.client(service_name=settings.SERVICE_NAME,
                          region_name=settings.REGION_NAME,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          endpoint_url=settings.ENDPOINT_URL)

        s3.upload_file(file, 'sp-at', f'regalii/{archname}')
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': 'sp-at',
                                                'Key': f'regalii/{archname}'})
        return url

