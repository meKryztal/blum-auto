import os
import sys
import time
import json
import random
import requests
import argparse
from json import dumps as dp
from datetime import datetime
from colorama import *
from urllib.parse import parse_qs
from base64 import b64decode
from fake_useragent import UserAgent

init(autoreset=True)

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
hitam = Fore.LIGHTBLACK_EX
magenta = Fore.LIGHTMAGENTA_EX


class BlumTod:
    def __init__(self):
        self.base_headers = {
            "accept": "application/json, text/plain, */*",
            "user-agent": UserAgent(os='android').random,
            "content-type": "application/json",
            "origin": "https://telegram.blum.codes",
            "x-requested-with": "org.telegram.messenger",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "referer": "https://telegram.blum.codes/",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en,en-US;q=0.9",
        }
        self.garis = putih + "~" * 50

    def renew_access_token(self, tg_data):
        headers = self.base_headers.copy()
        data = dp(
            {
                "query": tg_data,
            },
        )
        headers["Content-Length"] = str(len(data))
        url = "https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
        res = self.http(url, headers, data)
        token = res.json().get("token")
        if token is None:
            self.log(f"{merah}'token' не найден, вставьте его в data.txt !!!")
            return 0

        access_token = token.get("access")

        return access_token

    def solve_task(self, access_token):
        url_task = "https://game-domain.blum.codes/api/v1/tasks"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        res = self.http(url_task, headers)
        for tasks in res.json():
            if isinstance(tasks, str):
                self.log(f"{kuning}Ошибка получения списка заданий")
                return
            for task in tasks.get("tasks"):
                # print(task)
                task_id = task.get("id")
                task_title = task.get("title")
                task_status = task.get("status")
                if task_status == "NOT_STARTED":
                    url_start = (
                        f"https://game-domain.blum.codes/api/v1/tasks/{task_id}/start"
                    )
                    res = self.http(url_start, headers, "")
                    if "message" in res.text:
                        continue

                    url_claim = (
                        f"https://game-domain.blum.codes/api/v1/tasks/{task_id}/claim"
                    )
                    res2 = self.http(url_claim, headers, "")

                    if "message" in res.text:
                        continue

                    status = res2.json().get("status")
                    if status == "FINISHED":
                        self.log(f"{hijau}Выполнил задание {task_title} ")
                        continue

    def set_proxy(self, proxy=None):
        self.ses = requests.Session()
        if proxy is not None:
            self.ses.proxies.update({"http": proxy, "https": proxy})

    def claim_farming(self, access_token):
        url = "https://game-domain.blum.codes/api/v1/farming/claim"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        res = self.http(url, headers, "")
        balance = res.json().get("availableBalance", 0)
        self.log(f"{hijau}Баланс после клейма : {putih}{balance}")
        return

    def get_balance(self, access_token, only_show_balance=False):
        url = "https://game-domain.blum.codes/api/v1/user/balance"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        while True:
            res = self.http(url, headers)
            balance = res.json().get("availableBalance", 0)
            self.log(f"{hijau}Баланс : {putih}{balance}")
            if only_show_balance:
                return
            timestamp = res.json().get("timestamp")
            if timestamp is None:
                self.countdown(3)
                continue
            timestamp = round(timestamp / 1000)
            if "farming" not in res.json().keys():
                return False, "not_started"
            end_farming = res.json().get("farming", {}).get("endTime")
            if end_farming is None:
                self.countdown(3)
                continue
            break
        end_farming = round(end_farming / 1000)
        if timestamp > end_farming:
            self.log(f"{hijau}Пришло время для клейма")
            return True, end_farming

        self.log(f"{kuning}Еще не пришло время для клейма")
        end_date = datetime.fromtimestamp(end_farming)
        self.log(f"{hijau}Конец фарминга : {putih}{end_date}")
        return False, end_farming

    def start_farming(self, access_token):
        url = "https://game-domain.blum.codes/api/v1/farming/start"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        while True:
            res = self.http(url, headers, "")
            end = res.json().get("endTime")
            if end is None:
                self.countdown(3)
                continue
            break

        end_date = datetime.fromtimestamp(end / 1000)
        self.log(f"{hijau}Запустил фарминг")
        self.log(f"{hijau}Конец фарминга : {putih}{end_date}")
        return round(end / 1000)

    def get_friend(self, access_token):
        url = "https://gateway.blum.codes/v1/friends/balance"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        res = self.http(url, headers)
        can_claim = res.json().get("canClaim", False)

        if can_claim:
            url_claim = "https://gateway.blum.codes/v1/friends/claim"
            res = self.http(url_claim, headers, "")
            if res.json().get("claimBalance") is not None:
                self.log(f"{hijau}Заклеймил рефералку")
                return
            self.log(f"{merah}Ошибка клейма рефералки")
            return

    def checkin(self, access_token):
        url = "https://game-domain.blum.codes/api/v1/daily-reward?offset=-420"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        res = self.http(url, headers)
        if res.status_code == 404:
            self.log(f"{kuning}Уже делал чекин сегодня")
            return
        res = self.http(url, headers, "")
        if "ok" in res.text.lower():
            self.log(f"{hijau}Сделал чекин")
            return

        self.log(f"{merah}Ошибка чекина")
        return

    def playgame(self, access_token):
        url_play = "https://game-domain.blum.codes/api/v1/game/play"
        url_claim = "https://game-domain.blum.codes/api/v1/game/claim"
        url_balance = "https://game-domain.blum.codes/api/v1/user/balance"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        while True:
            res = self.http(url_balance, headers)
            play = res.json().get("playPasses")
            if play is None:
                self.log(f"{kuning}Ошибка получения количества билетов")
                break
            self.log(f"{hijau}Билеты: {putih}{play}{hijau} шт")
            if play <= 0:
                return
            for i in range(play):
                if self.is_expired(access_token):
                    return True
                res = self.http(url_play, headers, "")
                game_id = res.json().get("gameId")
                if game_id is None:
                    message = res.json().get("message", "")
                    if message == "cannot start game":
                        self.log(
                            f"{kuning}{message}, попробую позже"
                        )
                        return False
                    self.log(f"{kuning}{message}")
                    continue
                while True:
                    self.countdown(30)
                    point = random.randint(self.MIN_WIN, self.MAX_WIN)
                    data = json.dumps({"gameId": game_id, "points": point})
                    res = self.http(url_claim, headers, data)
                    if "OK" in res.text:
                        self.log(
                            f"{hijau}Получил {putih}{point}{hijau} с игры !"
                        )

                        break

                    message = res.json().get("message", "")
                    if message == "game session not finished":
                        continue

                    self.log(f"{merah}Ошибка получения {putih}{point}{merah} с игры !")
                    break

    def data_parsing(self, data):
        return {k: v[0] for k, v in parse_qs(data).items()}

    def log(self, message):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{hitam}[{now}]{reset} {message}")

    def get_local_token(self, userid):
        if not os.path.exists("tokens.json"):
            open("tokens.json", "w").write(json.dumps({}))
        tokens = json.loads(open("tokens.json", "r").read())
        if str(userid) not in tokens.keys():
            return False

        return tokens[str(userid)]

    def save_local_token(self, userid, token):
        tokens = json.loads(open("tokens.json", "r").read())
        tokens[str(userid)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

    def is_expired(self, token):
        header, payload, sign = token.split(".")
        payload = b64decode(payload + "==").decode()
        jload = json.loads(payload)
        now = round(datetime.now().timestamp()) + 300
        exp = jload["exp"]
        if now > exp:
            return True

        return False

    def save_failed_token(self, userid, data):
        file = "auth_failed.json"
        if not os.path.exists(file):
            open(file, "w").write(json.dumps({}))

        acc = json.loads(open(file, "r").read())
        if str(userid) in acc.keys():
            return

        acc[str(userid)] = data
        open(file, "w").write(json.dumps(acc, indent=4))

    def load_config(self):
        try:

            self.AUTOGAME = input(f"{magenta}Играть в игру? {putih}(1 - Да, 2 - Нет)\n")
            self.DEFAULT_INTERVAL = 3                  # 3 секунды между аккаунтами
            if self.AUTOGAME=='1':
                self.MIN_WIN = int(input(f"{magenta}Введите минимальное значение очков с игры: \n"))
                self.MAX_WIN = int(input(f"{magenta}Введите максимальное значение очков с игры: \n"))

                if self.MIN_WIN > self.MAX_WIN:
                    self.log(f"{kuning}Максимальное значение очков с игры должно быть выше минимального.")
                    sys.exit()

        except ValueError:
            self.log(f"{merah}Ошибка ввода данных. Убедитесь, что введены числовые значения там, где это требуется.")
            sys.exit()

    def ipinfo(self):
        res = self.http("https://ipinfo.io/json", {"content-type": "application/json"})
        if res is False:
            return False
        if res.status_code != 200:
            self.log(f"{merah}failed fetch ipinfo !")
            return False
        city = res.json().get("city")
        country = res.json().get("country")
        region = res.json().get("region")
        self.log(
            f"{biru}Проверка прокси: {hijau}Страна : {putih}{country} {hijau}Город : {putih}{city}"
        )
        return True

    def http(self, url, headers, data=None):
        while True:
            try:

                if data is None:
                    res = self.ses.get(url, headers=headers, timeout=30)
                elif data == "":
                    res = self.ses.post(url, headers=headers, timeout=30)
                else:
                    res = self.ses.post(url, headers=headers, data=data, timeout=30)

                return res

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                self.log(f"{merah}Ошибка подключения/тайм-аут соединения, проверь прокси!")

            except requests.exceptions.ProxyError:
                self.log(f"{merah}Ошибка прокси, проверь формат")
                return False

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"{putih}Жду {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def main(self):

        arg = argparse.ArgumentParser()

        arg.add_argument(
            "--data", help="Custom data input (default: data.txt)", default="data.txt"
        )
        arg.add_argument(
            "--proxy",
            help="custom proxy file input (default: proxies.txt)",
            default="proxies.txt",
        )
        args = arg.parse_args()

        if not os.path.exists(args.data):
            self.log(f"{merah}{args.data} не найден, введи правильное название !")
            sys.exit()

        datas = [i for i in open(args.data, "r").read().splitlines() if len(i) > 0]
        proxies = [i for i in open(args.proxy).read().splitlines() if len(i) > 0]
        use_proxy = True if len(proxies) > 0 else False
        self.log(f"{hijau}Всего аккаунтов : {putih}{len(datas)}")
        self.log(f"{biru}Использовать прокси : {putih}{use_proxy}")
        if len(datas) <= 0:
            self.log(f"{merah}Добавь сначала ключи в {args.data} ")
            sys.exit()
        print(self.garis)
        while True:
            list_countdown = []
            for no, data in enumerate(datas):
                self.log(f"{hijau}Номер аккаунта - {putih}{no + 1}")
                data_parse = self.data_parsing(data)
                user = json.loads(data_parse["user"])
                userid = user["id"]
                self.log(f"{hijau}Аккаунт : {putih}{user['username']}")
                if use_proxy:
                    proxy = proxies[no % len(proxies)]
                self.set_proxy(proxy if use_proxy else None)
                self.ipinfo() if use_proxy else None
                access_token = self.get_local_token(userid)
                failed_fetch_token = False
                while True:
                    if access_token is False:
                        access_token = self.renew_access_token(data)
                        if access_token is False:
                            self.save_failed_token(userid, data)
                            failed_fetch_token = True
                            break
                        self.save_local_token(userid, access_token)
                    expired = self.is_expired(access_token)
                    if expired:
                        access_token = False
                        continue
                    break
                if failed_fetch_token:
                    continue
                self.checkin(access_token)
                self.get_friend(access_token)
                self.solve_task(access_token)
                status, res_bal = self.get_balance(access_token)
                if status:
                    self.claim_farming(access_token)
                    res_bal = self.start_farming(access_token)
                if isinstance(res_bal, str):
                    res_bal = self.start_farming(access_token)
                list_countdown.append(res_bal)
                if self.AUTOGAME=='1':
                    while True:
                        result = self.playgame(access_token)
                        if result:
                            access_token = self.renew_access_token(data)
                            self.save_local_token(userid, access_token)
                            continue
                        break
                print(self.garis)
                self.countdown(self.DEFAULT_INTERVAL)
            min_countdown = min(list_countdown)
            now = int(time.time())
            result = min_countdown - now
            if result <= 0:
                continue

            self.countdown(result)


if __name__ == "__main__":
    try:
        app = BlumTod()
        app.load_config()
        app.main()
    except KeyboardInterrupt:
        sys.exit()
