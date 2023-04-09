from kavenegar import *
import requests
from bs4 import BeautifulSoup
import sys
import urllib3
import time
urllib3.disable_warnings()

# the url contains type and cities
# available_to_book=179 (directly book)
# city=24%2C25 =  Amsterdam (24) and Rotterdam (25) and Haarlem (616)
url = "https://holland2stay.com/residences.html?available_to_book=179&city=24%2C25%2C616"
receptor = ""
api_key = ""

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


def sendSMS(code):
    api = KavenegarAPI(api_key)
    params = {
        'template': 'code',
        'token': code,
        'receptor': receptor,
        'token2': '',
        'token3': '',
        'type': 'sms'
    }
    api.verify_lookup(params)


def makeCall():
    api = KavenegarAPI(api_key)
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
                if (price < 1600):  # for gross salary purposes
                    i = len(priceTag)
                    hasOption = True

            if (hasOption):
                print("[+] Perfect, sending SMS...")
                sendSMS("AVAILABLE")
                makeCall()
            else:
                print("[-] Not suitable!")

        except Exception as e:
            print("[error]: {}".format(e))
            sys.exit()
    else:
        print("[-] Not found")


counter = 300
while (True):
    checkDirectTag()
    print("---- | ---- =>", counter)
    counter = counter + 1
    if (counter >= 300):
        sendSMS("STILL_RUNNING")
        counter = 0

    time.sleep(200)
