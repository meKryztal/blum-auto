# Автофарм Blum

![photo_2024-09-03_20-09-38](https://github.com/user-attachments/assets/cd699bd0-b469-4394-bac8-8ae5c7d6f4da)


-  Клеймит каждые 8 часов поинты
-  Забирает дейли ревард
-  Можно загрузить сотни акков
-  Работа по ключу, без авторизации
-  Играет в игру
-  Выполняет задания
-  Забирает рефералку

  
### Что б использовать прокси, просто вставьте их в файл proxies.txt
```
http://127.0.0.1:6969
http://user:pass@127.0.0.1:6969
socks5://127.0.0.1:6969
socks5://user:pass@127.0.0.1:6969
```


# Установка:
1. Установить python (Протестировано на 3.11)

2. Зайти в cmd(терминал) и вписывать
   Если сказали на раб стол винды
   ```
   cd Desktop
   ```
Если в другом месте, то ищите свой путь   

Переходим в папку скрипта:
   ```
   cd blum-auto
   ```
4. Установить модули
   
   ```
   pip install -r requirements.txt
   ```
 
   или
   
   ```
   pip3 install -r requirements.txt
   ```



5. Запуск
   ```
   python blum.py
   ```

   или

   ```
   python3 blum.py
   ```

   
# Или через Pycharm ГАЙД на любых системах и решения ошибок внизу гайда
https://telegra.ph/Avtoklikker-dlya-BLUM-GAJD-05-29
   


## Вставить в файл data ключи такого вида, каждый новый ключ с новой строки:
   ```
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   ```
Вместо query_id= может быть user=, разницы нету
# Как получить query_id:
Заходите в telegram web, открываете бота, жмете F12 или в десктопной версии нужно зайти в настройки, доп настройки, экспериментальные настройки и включить "Enable webview inspecting", тогда при нажатии F12 у вас откроется окно, переходите в Application, в правой колонке находите query_id=бла бла бла или user=

![Без имени](https://github.com/user-attachments/assets/1a0b4651-f472-4444-9b8b-42939fe3db1b)



