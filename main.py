import os
from dotenv import load_dotenv
from kavenegar import *
import requests
from bs4 import BeautifulSoup
import sys
import urllib3
import time
urllib3.disable_warnings()

load_dotenv()

# the url contains type and cities
# available_to_book=179 (directly book)
cities = os.getenv('CITIES').split(",")
normal_url = "https://holland2stay.com/residences.html"
student_only_url = "https://holland2stay.com/residences/studentonly.html"
student_only = True if os.getenv('STUDENT_ONLY') == "YES" else False

url = f"{student_only_url if os.getenv('STUDENT_ONLY') == 'YES' else normal_url}?available_to_book=179&city=" + \
    "%2C".join(cities)


receptors = os.getenv('RECEPTORS').split(",")
api = KavenegarAPI(os.getenv('KAVE_NEGAR_API'))

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1"
}


def sendMessage(code):

    for receptor in receptors:
        params = {
            'template': 'code',
            'token': code,
            'receptor': receptor,
            'token2': '',
            'token3': '',
            'type': 'sms'
        }
        api.verify_lookup(params)


def availableOptionNotify():
    sendMessage("AVAILABLE_VP")

    for receptor in receptors:
        params = {
            'template': 'call',
            'token': "1234",
            'receptor': receptor,
            'type': 'call'
        }
        api.verify_lookup(params)


def checkDirectTag():
    r = requests.session()
    print("[*] Checking")

    try:
        res = r.get(url, headers=HEADERS, verify=False)
    except Exception as e:
        print("[error]: {}".format(e))
        sys.exit()

    soup = BeautifulSoup(res.content, features="html.parser")
    # directTag = soup.find_all('span', {'class': 'direct-tag'})
    priceTag = soup.find_all('div', {'class': 'price'})
    # itemTag = soup.find_all('div', {'class': 'regi-item'})

    if (len(priceTag) > 0):
        try:
            i = 0
            hasOption = False
            print("[+] Found something")

            while (i <= len(priceTag) - 1):
                price = int(
                    ''.join(filter(str.isdigit, priceTag[i].text.split(".")[0])))
                i = i+1
                if (price < int(os.getenv('BASIC_RENT'))):
                    i = len(priceTag)
                    hasOption = True

            if (hasOption):
                print("[+] Perfect, notify availibility...")
                availableOptionNotify()
            else:
                print("[-] Not suitable!")

        except Exception as e:
            print("[error]: {}".format(e))
            sys.exit()
    else:
        print("[-] Not found")


counter = 180
while (True):
    checkDirectTag()
    print("---- | ---- =>", counter)
    print("URL -> ", url)
    counter = counter + 1
    if (counter >= 180):
        sendMessage("Alive")
        counter = 0

    time.sleep(200)
