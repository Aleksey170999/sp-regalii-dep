import requests as requests


files = {'file': open('regs.xlsx', 'rb')}
data = {"fio": "Тихонов Алексей Владимирович",
        "city": "Москва",
        "regalia": "Проф. Тихонов Алексей Владимирович (Москва)"}

r = requests.post('http://127.0.0.1:8000/regals/',
                  files=files)


print(r.json())
