# Автофарм Blum



-  Клеймит каждые 8 часов поинты
-  Забирает дейли ревард
-  Можно загрузить сотни акков
-  Работа по ключу, без авторизации
-  Играет в игру
-  Выполняет задания
-  Забирает рефералку
  



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
   


## Вставить в файл init_data ключи такого вида, каждый новый ключ с новой строки:
   ```
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   ```
Вместо query_id= может быть user=, разницы нету
# Как получить query_id:
Заходите в telegram web, открываете бота, жмете F12 или в десктопной версии открывайте окно, правой кнопкой жмете и выбираете самое нижнее "проверить" и переходите в Application, в правой колонке находите query_id=бла бла бла или user=

![Без имени](https://github.com/user-attachments/assets/1a0b4651-f472-4444-9b8b-42939fe3db1b)



