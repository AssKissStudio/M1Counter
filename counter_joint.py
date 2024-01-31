import requests, json, wget, os
from colorama import init, Fore
init(autoreset=True)
c1 = 0
t1me = 0

def login():
    global c1, acs_tkn
    acs_tkn = Fore.LIGHTYELLOW_EX + 'Здесь должен быть ваш токен'
    while c1 == 0:
        mail = input(Fore.BLUE + "Введите почту(F - если из файла) или токен:")
        if len(mail) == 32:
            acs_tkn = mail
            c1 = 1
        elif mail.count('@') == 1:
            pw = input(Fore.BLUE + "Введите пароль:")
            if len(pw) < 8:
                print(Fore.RED + 'Неверный формат пароля')
            else:
                lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={mail}&password={pw}").json()
                if lrqst['code'] == 0:
                    c1 = 1
                    acs_tkn = lrqst['data']['access_token']
                    return acs_tkn
                else:
                    err = lrqst['code']
                    print(Fore.RED + f'Код ошибки: {err}')
        elif mail == 'F':
            read()
            mail = maild
            pw = pwd
            lrqst = requests.get(f"https://monopoly-one.com/api/auth.signin?email={mail}&password={pw}").json()
            if lrqst['code'] == 0:
                c1 = 1
                acs_tkn = lrqst['data']['access_token']
            else:
                err = lrqst['code']
                print(Fore.RED + f'Код ошибки: {err}')
        else:
            print(Fore.RED + 'Неверный формат данных')
        print(Fore.LIGHTYELLOW_EX + acs_tkn)


def read():
    global maild, pwd, idd
    with open("config.txt") as file:
        str = file.read()
        dicti = json.loads(str)
    if bool(dicti['email']) == 1 & bool(dicti['password']) == 1:
        maild = dicti['email']
        pwd = dicti['password']

def moneycount():
    while True:
        uid = input(Fore.BLUE + 'Введите id аккаунта:')
        fee = int(input(Fore.BLUE + 'Учитывать комиссию продажи?'))
        chest = []
        summ = 0
        bag = set()
        inventory = requests.get(f'https://monopoly-one.com/api/inventory.get?access_token={acs_tkn}&user_id={uid}').json()['data']['things']
        for thing in inventory:
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
                    #print(price)
                    if str(int(price*100)).isdigit():
                        price += 0.001
                        price = round(price,2)
                        #print(price)
                        if fee == 1:
                            price = round(price * 0.85, 2)
                        cost = round(price*chest.count(item),2)
                        print(Fore.LIGHTBLACK_EX + f'{item}: {cost}₽')
                        summ += cost
        print(Fore.GREEN + f'{round(summ,2)}₽')

def config():
    if not os.path.exists('config.txt'):
        wget.download('https://raw.githubusercontent.com/AssKissStudio/M1Config/main/config.txt')
        print('==> Загружен файл параметров. Вы можете изменить его в любом текстовом редакторе')

print(Fore.LIGHTWHITE_EX + 'Counter. Made by AssKiss Studio https://github.com/AssKissStudio/M1Counter')
config()
login()
moneycount()