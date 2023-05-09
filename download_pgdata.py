import requests
import zipfile

resp_for_link = requests.get("https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key=" + "https://disk.yandex.ru/d/2ehFN4VNvq1P2A")
if resp_for_link.status_code != 200:
    raise requests.RequestException()

link = resp_for_link.json().get('href')

resp = requests.get(link)

if resp.status_code != 200:
    raise requests.RequestException()


filename = 'pgdata.zip'

with open(filename, 'wb') as f:
    f.write(resp.content)

with zipfile.ZipFile(filename, 'r') as zip:
    zip.extractall('pgdata/')

print('Successfully downloaded pgdata')
