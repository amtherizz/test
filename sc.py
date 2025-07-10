import requests
import bs4

print(bs4.BeautifulSoup(requests.get('https://infopriangan.com/sekjen-atr-bpn-buka-rapat-evaluasi-proyek-ilasp-2025-2029/').text,'html.parser').text)