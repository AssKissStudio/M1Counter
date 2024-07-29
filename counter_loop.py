import requests, json, wget, os,time,random
from audioplayer import AudioPlayer
from colorama import init, Fore
init(autoreset=True)
c1 = 0
t1me = 0

def login():
    global c1, acs_tkn, rfr_tkn, uid
    acs_tkn = Fore.LIGHTYELLOW_EX + 'Здесь должен быть ваш токен'
    while c1 == 0:
        mail = input(Fore.MAGENTA + "Введите почту(F - если из файла) или токен:")
        if len(mail) == 32:
            acs_tkn = mail
            c1 = 2
        elif mail.count('@') == 1:
            pw = input(Fore.MAGENTA + "Введите пароль:")
            if len(pw) < 8:
                print(Fore.RED + 'Неверный формат пароля')
            else:
                lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={mail}&password={replaces(pw)}").json()
                if 'data' in lrqst:
                    if lrqst['code'] == 0:
                        if 'totp_session_token' in lrqst['data']:
                            tfa = ''
                            while True:
                                while tfa == "":
                                    tfa = input('Введите код 2FA:')
                                else:
                                    auth2 = requests.get(f'https://monopoly-one.com/api/auth.totpVerify?totp_session_token={lrqst["data"]["totp_session_token"]}&code={tfa}').json()
                                    if auth2['code'] == 0:
                                        c1 = 1
                                        acs_tkn = auth2['data']['access_token']
                                        rfr_tkn = auth2['data']['refresh_token']
                                        uid = auth2['data']['user_id']
                                        return acs_tkn, rfr_tkn, uid
                                    else:
                                        print(Fore.RED + 'Ошибка')
                                        tfa = ''
                        else:
                            c1 = 1
                            acs_tkn = lrqst['data']['access_token']
                            rfr_tkn = lrqst['data']['refresh_token']
                            uid = lrqst['data']['user_id']
                            return acs_tkn, rfr_tkn, uid

                else:
                    err = lrqst['code']
                    print(Fore.RED + f'Код ошибки: {err}')
        elif mail == 'F':
            read()
            lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={maild}&password={replaces(pwd)}").json()
            #print(lrqst)
            if 'data' in lrqst:
                if lrqst['code'] == 0:
                    if 'totp_session_token' in lrqst['data']:
                        tfa = ''
                        while True:
                            while tfa == "":
                                tfa = input('Введите код 2FA:')
                            else:
                                auth2 = requests.get(
                                    f'https://monopoly-one.com/api/auth.totpVerify?totp_session_token={lrqst["data"]["totp_session_token"]}&code={tfa}').json()
                                if auth2['code'] == 0:
                                    c1 = 1
                                    acs_tkn = auth2['data']['access_token']
                                    rfr_tkn = auth2['data']['refresh_token']
                                    uid = auth2['data']['user_id']
                                    return acs_tkn, rfr_tkn, uid
                                else:
                                    print(Fore.RED + 'Ошибка')
                                    tfa = ''
                    else:
                        c1 = 1
                        acs_tkn = lrqst['data']['access_token']
                        rfr_tkn = lrqst['data']['refresh_token']
                        uid = lrqst['data']['user_id']
                        return acs_tkn, rfr_tkn, uid
            else:
                err = lrqst['code']
                print(Fore.RED + f'Код ошибки: {err}')
        else:
            print(Fore.RED + 'Неверный формат данных')

def moneycount():
    while True:
        uid = input(Fore.MAGENTA + 'Введите id аккаунта:')
        nottosell = int(input(Fore.MAGENTA+'Учитывать стоимость вещей, которые нельзя продавать?'))
        fee = int(input(Fore.MAGENTA + 'Учитывать комиссию продажи?'))
        chest = []
        summ = 0
        bag = set()
        inventory = requests.get(f'https://monopoly-one.com/api/inventory.get?access_token={acs_tkn}&user_id={uid}').json()['data']['things']
        #print(inventory)
        for thing in inventory:
            #print(thing['can_sell'])
            if (not "can_sell" in thing)|(nottosell==1):
                chest.append(thing['thing_prototype_id'])
                bag.add(thing['thing_prototype_id'])
        #print(chest)
        #print(bag)
        for item in bag:
            if item in chest:
                #print(item)
                price = requests.get(f'https://monopoly-one.com/api/market.getBestPrice?access_token={acs_tkn}&thing_prototype_id={item}').json()
                #print(price)
                price = price['data']
                if 'price' in price:
                    price = price['price']
                    if price is not None:
                        #print(price)
                        #if str(int(price*100)).isdigit():
                        #print(price)
                        if fee == 1:
                            price = round((price * 0.85)+0.001, 2)
                        cost = round(price*chest.count(item)+0.001,2)
                        print(Fore.LIGHTBLACK_EX + f'{item}: {cost}₽')
                        summ += cost
                    else:
                        print(Fore.RED + f'Вещь с id {item} пока не продают.')
        print(Fore.GREEN + f'{round(summ,2)}₽')
        print(Fore.LIGHTWHITE_EX+f'Стоимость аккаунта актуальна на {time.strftime("%a, %d %b %Y %H:%M:%S",time.localime())}')

def read():
    global maild, pwd, idd
    with open("config.txt",'r',-1,'utf-8') as file:
        str = file.read()
        dicti = json.loads(str)
    if bool(dicti['email']) == 1 & bool(dicti['password']) == 1:
        maild = dicti['email']
        pwd = dicti['password']


def config():
    if not os.path.exists('config.txt'):
        wget.download('https://raw.githubusercontent.com/AssKissStudio/M1Config/main/config.txt')
        print('==> Загружен файл параметров. Вы можете изменить его в любом текстовом редакторе')

def error():
    print('Токен недействителен, либо лимиты')
    if not os.path.exists('error.mp3'):
        wget.download('https://raw.githubusercontent.com/AssKissStudio/M1Config/main/error.mp3')
    AudioPlayer('error.mp3').play(block=True)
    os.remove('error.mp3')
    exit()

def refresh():
    global acs_tkn,rfr_tkn
    if c1 == 1:
        refreshh = requests.get(f'https://monopoly-one.com/api/auth.refresh?refresh_token={rfr_tkn}').json()
        if refreshh['code'] == 0:
            print('Обновил токены')
            acs_tkn = refreshh['data']['access_token']
            rfr_tkn = refreshh['data']['refresh_token']
            time.sleep(random.randint(400,800)/100)
            return acs_tkn,rfr_tkn
    else:
        error()

def replaces(var):
    var = var.replace('!','%21')
    var = var.replace('\"', '%22')
    var = var.replace('#', '%23')
    var = var.replace('$', '%24')
    var = var.replace('&', '%26')
    var = var.replace('\'', '%27')
    var = var.replace('(', '%28')
    var = var.replace(')', '%29')
    var = var.replace('!', '%21')
    var = var.replace('*', '%2A')
    var = var.replace('+', '%2B')
    var = var.replace('/', '%2F')
    return var



print(Fore.LIGHTWHITE_EX + 'Counter. Made by AssKiss Studio https://github.com/AssKissStudio/M1Counter')
config()
login()
while True:
    try:
        moneycount()
    except:
        if c1 == 1:
            refresh()
        else:
            error()