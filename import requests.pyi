import requests


def location(ip: str):
    response = requests.get(f"http://ip-api.com/json/{ip}?lang=ru").json()
    print("країна:", response['country'])
    print("код страни:", response['countryCode' ])
    print ("регіон", response ['region'])
    print("імя регіона", response['regionName'])
    print("город", response['city'])
    print("індекс", response['zip'])
    print("кординати(ширина):",  response['lat'])
    print ("Координаты (высота):",  response['lon'])
    print ("часовий пояс:", response['timezone'])
    print ("провайдер", response['isp'])

answer = input("BBepиTe IP-aдpec: ") 
location(answer)























